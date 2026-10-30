from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    ciudad_id = fields.Many2one("res.country.state.ciudad", string="Ciudad", tracking=True, index=True)
    municipio_id = fields.Many2one("res.country.state.municipio", string="Municipio", tracking=True, index=True)
    colonia_id = fields.Many2one("res.country.state.municipio.colonia", string="Colonia", tracking=True, index=True)
    l10n_mx_edi_colony = fields.Char(string="Colonia fiscal", related="colonia_id.name", readonly=True)

    @api.onchange("ciudad_id")
    def _onchange_ciudad_id(self):
        for partner in self:
            if partner.ciudad_id:
                partner.city = partner.ciudad_id.name
                state = partner.ciudad_id.state_id
                if state:
                    partner.state_id = state
                    partner.country_id = state.country_id
                if partner.municipio_id and partner.municipio_id.ciudad_id != partner.ciudad_id:
                    partner.municipio_id = False
                    partner.colonia_id = False

    @api.onchange("municipio_id")
    def _onchange_municipio_id(self):
        for partner in self:
            if partner.municipio_id:
                municipality = partner.municipio_id
                partner.ciudad_id = municipality.ciudad_id
                partner.state_id = municipality.state_id
                partner.country_id = municipality.state_id.country_id
                if partner.ciudad_id:
                    partner.city = partner.ciudad_id.name
                if partner.colonia_id and partner.colonia_id.municipio_id != municipality:
                    partner.colonia_id = False

    @api.onchange("colonia_id")
    def _onchange_colonia_id(self):
        for partner in self:
            if partner.colonia_id:
                municipality = partner.colonia_id.municipio_id
                partner.municipio_id = municipality
                partner.ciudad_id = municipality.ciudad_id
                partner.state_id = municipality.state_id
                partner.country_id = municipality.state_id.country_id
                partner.zip = partner.colonia_id.cp
                if partner.ciudad_id:
                    partner.city = partner.ciudad_id.name
