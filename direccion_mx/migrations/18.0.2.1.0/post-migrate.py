"""Materialize missing legacy related text without replacing any existing text.

Run by Odoo's upgrade loader only in an approved disposable upgrade rehearsal.
The table/ID/relation snapshot must be compared before and after that rehearsal.
"""


def migrate(cr, version):
    cr.execute("""
        UPDATE res_partner AS p SET city = c.name
        FROM res_country_state_ciudad c
        WHERE p.ciudad_id = c.id AND p.city IS NULL
    """)
    cr.execute("""
        UPDATE res_partner AS p SET l10n_mx_edi_colony = c.name
        FROM res_country_state_municipio_colonia c
        WHERE p.colonia_id = c.id AND p.l10n_mx_edi_colony IS NULL
    """)
