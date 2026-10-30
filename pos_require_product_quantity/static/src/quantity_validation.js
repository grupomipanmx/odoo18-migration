/** @odoo-module **/
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0.html).

export function invalidQuantityLines(order, enabled) {
    if (!enabled || !order) {
        return [];
    }
    // Keep legitimate fractional sales and negative refund quantities.
    return order.lines.filter((line) => !Number.isFinite(line.qty) || line.qty === 0);
}
