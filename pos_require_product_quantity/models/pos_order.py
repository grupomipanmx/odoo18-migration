# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).
import math

from odoo import api, models, _
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _check_required_product_quantities(self):
        for order in self:
            if order.config_id.require_product_quantity and any(
                line.qty == 0 or not math.isfinite(line.qty) for line in order.lines
            ):
                raise ValidationError(_("Enter a non-zero quantity for every order line before payment."))

    def _process_saved_order(self, draft):
        # Validate outside core's action_pos_order_paid try/except: core catches
        # non-database exceptions there and can continue to create a picking.
        if not draft and self.state != "cancel":
            self._check_required_product_quantities()
        return super()._process_saved_order(draft)

    @api.constrains("state", "lines", "config_id")
    def _check_finalized_quantities(self):
        self.filtered(lambda order: order.state in ("paid", "done", "invoiced"))._check_required_product_quantities()


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.constrains("qty", "order_id")
    def _check_finalized_order_quantities(self):
        self.order_id._check_finalized_quantities()
