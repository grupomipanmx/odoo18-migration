// Exercise the production patch bodies with explicit service/base-class doubles.
// These tests do not load OWL, the real patch utility, a browser or an Odoo server.
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const dataModule = (source) => "data:text/javascript;base64," + Buffer.from(source).toString("base64");
const patchURL = dataModule(`export const patches = [];
export function patch(target, extension) { Object.setPrototypeOf(extension, target); patches.push({target, extension}); }`);
const storeURL = dataModule(`export class PosStore { async pay() { this.events.push("base-pay"); return "payment-screen"; } }`);
const screenURL = dataModule(`export class PaymentScreen { async validateOrder(force) { this.events.push("base-validate:" + force); return "validated"; } }`);
const quantitySource = await readFile(new URL("../pos_require_product_quantity/static/src/quantity_validation.js", import.meta.url), "utf8");
const replacements = {
    "@web/core/utils/patch": patchURL,
    "@web/core/l10n/translation": dataModule("export const _t = (message) => message;"),
    "@web/core/confirmation_dialog/confirmation_dialog": dataModule("export class AlertDialog {}"),
    "@point_of_sale/app/store/pos_store": storeURL,
    "@point_of_sale/app/screens/payment_screen/payment_screen": screenURL,
    "@pos_require_product_quantity/quantity_validation": dataModule(quantitySource),
};
let productionSource = await readFile(new URL("../pos_require_product_quantity/static/src/payment_guard.js", import.meta.url), "utf8");
for (const [name, url] of Object.entries(replacements)) {
    productionSource = productionSource.replaceAll(JSON.stringify(name), JSON.stringify(url));
}
await import(dataModule(productionSource));
const { patches } = await import(patchURL);
const pay = patches[0].extension.pay;
const validate = patches[1].extension.validateOrder;

function context(qty, enabled = true) {
    const order = { lines: [{ qty }] };
    const events = [];
    const dialog = { add: () => events.push("warning") };
    return { events, dialog, order, get_order: () => order, currentOrder: order,
             config: { require_product_quantity: enabled },
             pos: { config: { require_product_quantity: enabled } },
             numberBuffer: { capture: () => events.push("capture") } };
}

test("zero quantity never calls the standard payment flow", async () => {
    const ctx = context(0);
    await pay.call(ctx);
    assert.deepEqual(ctx.events, ["capture", "warning"]);
});
test("valid sale calls the base payment flow after capture", async () => {
    const ctx = context(0.5);
    assert.equal(await pay.call(ctx), "payment-screen");
    assert.deepEqual(ctx.events, ["capture", "base-pay"]);
});
test("pending number-buffer value is checked before payment", async () => {
    const ctx = context(1);
    ctx.numberBuffer.capture = () => { ctx.events.push("capture"); ctx.order.lines[0].qty = 0; };
    await pay.call(ctx);
    assert.deepEqual(ctx.events, ["capture", "warning"]);
});
test("direct validation is blocked before standard removal/payment code", async () => {
    const ctx = context(0);
    await validate.call(ctx, true);
    assert.deepEqual(ctx.events, ["capture", "warning"]);
});
test("refund validation delegates arguments to standard behavior", async () => {
    const ctx = context(-1);
    assert.equal(await validate.call(ctx, true), "validated");
    assert.deepEqual(ctx.events, ["capture", "base-validate:true"]);
});
test("disabled flag allows both normal entry points", async () => {
    const ctx = context(0, false);
    await pay.call(ctx);
    await validate.call(ctx, false);
    assert.deepEqual(ctx.events, ["capture", "base-pay", "capture", "base-validate:false"]);
});
