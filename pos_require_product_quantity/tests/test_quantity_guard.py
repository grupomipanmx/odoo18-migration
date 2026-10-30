from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon


@tagged("post_install", "-at_install")
class TestQuantityGuard(TestPointOfSaleCommon):
    def setUp(self):
        super().setUp()
        self.pos_config.require_product_quantity = True
        self.session = self.env["pos.session"].create({"config_id": self.pos_config.id})

    def make_order(self, qty):
        return self.env["pos.order"].create({
            "session_id": self.session.id, "amount_tax": 0, "amount_total": 0,
            "amount_paid": 0, "amount_return": 0,
            "lines": [Command.create({"product_id": self.led_lamp.id, "qty": qty,
                                      "price_unit": 0, "price_subtotal": 0, "price_subtotal_incl": 0})],
        })

    def test_draft_can_sync_zero_quantity_but_cannot_finalize(self):
        order = self.make_order(0)
        self.assertEqual(order.state, "draft")
        with self.assertRaises(ValidationError):
            order._process_saved_order(False)
        self.assertEqual(order.state, "draft")
        self.assertFalse(order.picking_ids)

    def test_disabled_configuration_preserves_standard_behavior(self):
        self.pos_config.require_product_quantity = False
        self.make_order(0)._check_required_product_quantities()

    def test_fractional_sale_and_negative_refund_are_allowed(self):
        self.make_order(0.5)._check_required_product_quantities()
        self.make_order(-1)._check_required_product_quantities()

    def test_rpc_cannot_set_zero_quantity_order_paid(self):
        order = self.make_order(0)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            order.write({"state": "paid"})
