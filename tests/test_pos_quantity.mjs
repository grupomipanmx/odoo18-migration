import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { test } from "node:test";

const source = await readFile(new URL("../pos_require_product_quantity/static/src/quantity_validation.js", import.meta.url), "utf8");
const { invalidQuantityLines } = await import("data:text/javascript;base64," + Buffer.from(source).toString("base64"));

test("blocks zero quantities", () => {
    const zero = { qty: 0 };
    assert.deepEqual(invalidQuantityLines({ lines: [zero, { qty: 1 }] }, true), [zero]);
});
test("configuration disabled keeps the standard flow", () => {
    assert.deepEqual(invalidQuantityLines({ lines: [{ qty: 0 }] }, false), []);
});
test("allows fractional quantities and refunds", () => {
    assert.deepEqual(invalidQuantityLines({ lines: [{ qty: 0.5 }, { qty: -1 }] }, true), []);
});
test("rejects non-finite and malformed quantities", () => {
    const lines = [NaN, Infinity, undefined, "1"].map((qty) => ({ qty }));
    assert.deepEqual(invalidQuantityLines({ lines }, true), lines);
});
test("handles absent and empty orders", () => {
    assert.deepEqual(invalidQuantityLines(null, true), []);
    assert.deepEqual(invalidQuantityLines({ lines: [] }, true), []);
});
