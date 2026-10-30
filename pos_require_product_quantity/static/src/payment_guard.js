/** @odoo-module **/
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { invalidQuantityLines } from "@pos_require_product_quantity/quantity_validation";

function showQuantityWarning(dialog) {
    dialog.add(AlertDialog, {
        title: _t("Missing quantities"),
        body: _t("Enter a non-zero quantity for every order line before payment."),
    });
}

patch(PosStore.prototype, {
    async pay() {
        this.numberBuffer.capture();
        if (invalidQuantityLines(this.get_order(), this.config.require_product_quantity).length) {
            showQuantityWarning(this.dialog);
            return;
        }
        return super.pay(...arguments);
    },
});

patch(PaymentScreen.prototype, {
    async validateOrder() {
        this.numberBuffer.capture();
        if (invalidQuantityLines(this.currentOrder, this.pos.config.require_product_quantity).length) {
            showQuantityWarning(this.dialog);
            return;
        }
        return super.validateOrder(...arguments);
    },
});
