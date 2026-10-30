"""Read-only ORM snapshot and offline comparison; never connects to a database.

Call snapshot(env) from an authorized read-only Odoo 14/18 disposable shell.
Store snapshots outside Git. The CLI only compares existing JSON files.
"""
import argparse
import hashlib
import json
from pathlib import Path


FIELDS = {
    "res.country.state.cp": ["name", "state_id", "ciudad_id", "municipio_id"],
    "res.country.state.ciudad": ["name", "state_id", "clave_sat"],
    "res.country.state.municipio": ["name", "state_id", "ciudad_id", "clave_sat"],
    "res.country.state.municipio.colonia": ["name", "municipio_id", "cp", "clave_sat"],
    "res.partner": ["ciudad_id", "municipio_id", "colonia_id", "city", "l10n_mx_edi_colony",
                    "zip", "state_id", "country_id", "parent_id", "company_id", "active"],
}


def snapshot(env, batch_size=1000):
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    result = {"format": 1, "models": {}}
    for model_name, fields in FIELDS.items():
        model = env[model_name].sudo().with_context(active_test=False, lang=None, tz="UTC")
        fields = list(fields)
        if model_name == "res.partner" and "supplier_rank" in model._fields:
            fields.append("supplier_rank")
        missing = set(fields) - set(model._fields)
        if missing:
            raise ValueError(f"Missing fields for {model_name}: {sorted(missing)}")
        rows = {}
        last_id = 0
        while True:
            records = model.search([("id", ">", last_id)], order="id", limit=batch_size)
            if not records:
                break
            for row in records.read(["id"] + fields, load=None):
                canonical = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                rows[str(row["id"])] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
                last_id = row["id"]
        result["models"][model_name] = {"table": model._table, "fields": fields, "rows": rows}
    return result


def compare(before, after):
    errors = []
    if before.get("format") != 1 or after.get("format") != 1:
        return ["Unsupported snapshot format"]
    for name in FIELDS:
        old = before.get("models", {}).get(name)
        new = after.get("models", {}).get(name)
        if old is None or new is None:
            errors.append(f"{name}: missing model snapshot")
            continue
        if old.get("table") != new.get("table") or old.get("table") != name.replace(".", "_"):
            errors.append(f"{name}: table changed")
        if old.get("fields") != new.get("fields"):
            errors.append(f"{name}: field coverage changed")
        old_rows, new_rows = old.get("rows", {}), new.get("rows", {})
        if not old.get("fields") or not set(FIELDS[name]).issubset(old.get("fields", [])):
            errors.append(f"{name}: incomplete baseline fields")
        if set(old_rows) != set(new_rows):
            errors.append(f"{name}: IDs changed (removed={len(set(old_rows)-set(new_rows))}, "
                          f"added={len(set(new_rows)-set(old_rows))})")
        changed = sum(old_rows[key] != new_rows[key] for key in old_rows.keys() & new_rows.keys())
        if changed:
            errors.append(f"{name}: {changed} row fingerprints changed")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    args = parser.parse_args()
    errors = compare(json.loads(args.before.read_text(encoding="utf-8")),
                     json.loads(args.after.read_text(encoding="utf-8")))
    print(json.dumps({"result": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
