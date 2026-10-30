"""Validate the legacy schema before ORM initialization; never repair by deletion."""


def migrate(cr, version):
    required = {
        "res_country_state_cp": ("id", "name", "state_id", "ciudad_id", "municipio_id"),
        "res_country_state_ciudad": ("id", "name", "state_id"),
        "res_country_state_municipio": ("id", "name", "state_id", "ciudad_id"),
        "res_country_state_municipio_colonia": ("id", "name", "municipio_id", "cp"),
        "res_partner": ("id", "city", "ciudad_id", "municipio_id", "colonia_id"),
    }
    for table, columns in required.items():
        cr.execute("SELECT attname FROM pg_attribute WHERE attrelid = to_regclass(%s) "
                   "AND attnum > 0 AND NOT attisdropped", (table,))
        found = {row[0] for row in cr.fetchall()}
        if not set(columns).issubset(found):
            raise RuntimeError("direccion_mx: missing legacy table/columns: %s %s; "
                               "restore/inspect a disposable copy, do not recreate the catalog."
                               % (table, sorted(set(columns) - found)))
    # Queries contain only constant identifiers from this module, no user SQL.
    relations = [
        ("res_partner", "ciudad_id", "res_country_state_ciudad"),
        ("res_partner", "municipio_id", "res_country_state_municipio"),
        ("res_partner", "colonia_id", "res_country_state_municipio_colonia"),
        ("res_country_state_cp", "ciudad_id", "res_country_state_ciudad"),
        ("res_country_state_cp", "municipio_id", "res_country_state_municipio"),
        ("res_country_state_municipio", "ciudad_id", "res_country_state_ciudad"),
        ("res_country_state_municipio_colonia", "municipio_id", "res_country_state_municipio"),
    ]
    for table, column, target in relations:
        cr.execute(f"SELECT COUNT(*) FROM {table} a LEFT JOIN {target} b ON b.id = a.{column} "
                   f"WHERE a.{column} IS NOT NULL AND b.id IS NULL")
        if cr.fetchone()[0]:
            raise RuntimeError(f"direccion_mx: orphan references in {table}.{column}; no data was removed.")
