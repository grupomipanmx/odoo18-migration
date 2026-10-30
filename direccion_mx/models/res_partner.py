from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    ciudad_id = fields.Many2one("res.country.state.ciudad", string="Ciudad", tracking=True, index=True)
    municipio_id = fields.Many2one("res.country.state.municipio", string="Municipio", tracking=True, index=True)
    colonia_id = fields.Many2one("res.country.state.municipio.colonia", string="Colonia", tracking=True, index=True)
    # Preserve standard address text, including partners without MX catalogs.
    # Explicitly reset related/compute attributes if another definition supplied
    # them. Catalog selection fills omitted text; explicit imported text wins.
    city = fields.Char(related=False, compute=False, inverse=False, store=True, readonly=False)
    l10n_mx_edi_colony = fields.Char(
        string="Colonia fiscal", related=False, compute=False, inverse=False,
        store=True, readonly=False,
    )

    @api.model
    def _address_fields(self):
        return list(dict.fromkeys(super()._address_fields() + [
            "ciudad_id", "municipio_id", "colonia_id", "l10n_mx_edi_colony",
        ]))

    @api.model
    def _prepare_catalog_address_values(self, values, partner=None):
        values = dict(values)
        if not {"ciudad_id", "municipio_id", "colonia_id"}.intersection(values):
            return values

        # Only derive from explicitly selected catalogs. An unrelated write or
        # clearing a selector must not rewrite historical text or links.
        if values.get("colonia_id"):
            colony = self.env["res.country.state.municipio.colonia"].browse(values["colonia_id"])
            values.setdefault("municipio_id", colony.municipio_id.id)
            values.setdefault("zip", colony.cp)
            values.setdefault("l10n_mx_edi_colony", colony.name)
        if values.get("municipio_id"):
            municipality = self.env["res.country.state.municipio"].browse(values["municipio_id"])
            values.setdefault("ciudad_id", municipality.ciudad_id.id or False)
            values.setdefault("state_id", municipality.state_id.id)
            values.setdefault("country_id", municipality.state_id.country_id.id)
        if values.get("ciudad_id"):
            city = self.env["res.country.state.ciudad"].browse(values["ciudad_id"])
            values.setdefault("city", city.name)
            values.setdefault("state_id", city.state_id.id)
            values.setdefault("country_id", city.state_id.country_id.id)

        def selected(field, model):
            value = values.get(field, partner[field].id if partner else False)
            return self.env[model].browse(value) if value else self.env[model]

        city = selected("ciudad_id", "res.country.state.ciudad")
        municipality = selected("municipio_id", "res.country.state.municipio")
        colony = selected("colonia_id", "res.country.state.municipio.colonia")
        state = selected("state_id", "res.country.state")
        country = selected("country_id", "res.country")
        # Reject new contradictory selections rather than silently replacing
        # existing contact/supplier relations. Historical unrelated edits pass.
        if colony and colony.municipio_id != municipality:
            raise ValidationError("La colonia debe pertenecer al municipio seleccionado.")
        if city and municipality and municipality.ciudad_id and municipality.ciudad_id != city:
            raise ValidationError("El municipio debe pertenecer a la ciudad seleccionada.")
        if any(record and record.state_id != state for record in (city, municipality)):
            raise ValidationError("La ciudad y el municipio deben pertenecer al estado seleccionado.")
        if state and state.country_id != country:
            raise ValidationError("El estado debe pertenecer al país seleccionado.")
        return values

    @api.model_create_multi
    def create(self, vals_list):
        return super().create([self._prepare_catalog_address_values(vals) for vals in vals_list])

    def write(self, vals):
        if not {"ciudad_id", "municipio_id", "colonia_id"}.intersection(vals):
            return super().write(vals)
        # Prepare each record first because existing free-text values may differ.
        # Then batch records with identical values so ORM recomputations, tracking,
        # constraints and inherited write overrides retain normal recordset behavior.
        groups = []
        for partner in self:
            prepared = self._prepare_catalog_address_values(vals, partner=partner)
            for group in groups:
                if group[0] == prepared:
                    group[1] |= partner
                    break
            else:
                groups.append([prepared, partner])
        for prepared, partners in groups:
            super(ResPartner, partners).write(prepared)
        return True

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
                partner.l10n_mx_edi_colony = partner.colonia_id.name
                if partner.ciudad_id:
                    partner.city = partner.ciudad_id.name
