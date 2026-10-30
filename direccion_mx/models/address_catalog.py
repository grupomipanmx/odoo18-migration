import re

from odoo import api, fields, models


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
    def _name_search(self, name, domain=None, operator="ilike", limit=100, order=None):
        domain = list(domain or [])
        if name:
            term = name.strip()
            if re.fullmatch(r"\\d{4,5}", term):
                domain = ["|", ("cp", operator, term), ("name", operator, term)] + domain
            else:
                domain = [("name", operator, term)] + domain
        records = self.search(domain, limit=limit, order=order)
        return [(rec.id, rec.display_name) for rec in records]
