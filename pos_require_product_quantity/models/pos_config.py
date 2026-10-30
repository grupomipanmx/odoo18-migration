# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    require_product_quantity = fields.Boolean(string="Require product quantity in POS", default=False)

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_to_load = super()._load_pos_data_fields(config_id)
        # An empty list means all fields, not no fields. Do not accidentally
        # replace the complete POS configuration with just our boolean.
        if not fields_to_load or "require_product_quantity" in fields_to_load:
            return fields_to_load
        return fields_to_load + ["require_product_quantity"]
