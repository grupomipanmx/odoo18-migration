import re

from odoo import api, fields, models
from odoo.osv import expression


class CodigoPostal(models.Model):
    _name = "res.country.state.cp"
    _table = "res_country_state_cp"
    _description = "Código postal de México"

    # Keep the legacy columns, size, optionality and relation targets. No data
    # loader or replacement table: an upgrade must reuse the existing records.
    name = fields.Char(string="Código postal", size=128)
    state_id = fields.Many2one("res.country.state", string="Estado")
    ciudad_id = fields.Many2one("res.country.state.ciudad", string="Localidad")
    municipio_id = fields.Many2one("res.country.state.municipio", string="Municipio")


class Ciudad(models.Model):
    _name = "res.country.state.ciudad"
    _table = "res_country_state_ciudad"
    _description = "Ciudad"
    _order = "name"

    state_id = fields.Many2one("res.country.state", string="Estado", required=True, index=True)
    municipio_ids = fields.One2many("res.country.state.municipio", "ciudad_id", string="Municipios")
    name = fields.Char(string="Nombre", size=256, required=True, index=True)
    clave_sat = fields.Char(string="Clave SAT")


class Municipio(models.Model):
    _name = "res.country.state.municipio"
    _table = "res_country_state_municipio"
    _description = "Municipio"
    _order = "name"

    state_id = fields.Many2one("res.country.state", string="Estado", required=True, index=True)
    ciudad_id = fields.Many2one("res.country.state.ciudad", string="Ciudad", index=True)
    name = fields.Char(string="Nombre", size=64, required=True, index=True)
    clave_sat = fields.Char(string="Clave SAT")

    @api.onchange("ciudad_id")
    def _onchange_ciudad_id(self):
        for rec in self:
            if rec.ciudad_id:
                rec.state_id = rec.ciudad_id.state_id


class Colonia(models.Model):
    _name = "res.country.state.municipio.colonia"
    _table = "res_country_state_municipio_colonia"
    _description = "Colonia"
    _order = "name"

    municipio_id = fields.Many2one("res.country.state.municipio", string="Municipio", required=True, index=True)
    name = fields.Char(string="Nombre", size=256, required=True, index=True)
    cp = fields.Char(string="Código postal", size=10, index=True)
    clave_sat = fields.Char(string="Clave SAT")

    @api.model
    def _search_display_name(self, operator, value):
        # Odoo 18 name_search searches display_name; _name_search is no longer
        # its extension point. Return a domain so caller filters and rules apply.
        if isinstance(value, str) and re.fullmatch(r"\d{4,5}", value.strip()):
            term = value.strip()
            combine = (
                expression.AND
                if operator in expression.NEGATIVE_TERM_OPERATORS
                else expression.OR
            )
            return combine([[("cp", operator, term)], [("name", operator, term)]])
        return super()._search_display_name(operator, value)
