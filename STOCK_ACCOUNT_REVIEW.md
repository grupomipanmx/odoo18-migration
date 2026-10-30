# Compras, inventario y contabilidad — 2026-10-30

Revisión de código, no validación contable de una base. Fuentes: stock_account_purchase `a3594d2ac577c0c491933ca743de46fcf20fb160`; Odoo 18 `54c0991d2949bf4090231c8c167b4a1038769085`. Enlaces en SOURCE_REVIEW.md.

## Hallazgos confirmados

1. El legado añade `res.partner.disable_move` y omite `_account_entry_move` cuando el proveedor de la compra tiene la bandera activa. Esto puede dejar capas de valoración sin sus asientos esperados; no es una simple extensión visual.
2. En Odoo 18 `_account_entry_move(qty, description, svl_id, cost)` conserva esos argumentos, pero retorna lista de valores de asientos. `stock.valuation.layer` concatena ese resultado con `am_vals += ...`. El retorno `False` del legado es incompatible con esa operación cuando se activa la bandera.
3. La cadena `picking_id.purchase_id` depende de `purchase_stock`, que define purchase_id. El manifiesto legado sólo declara account y stock_account: dependencia técnica incompleta. Revisar recepciones sin compra, devoluciones, múltiples compras/partner comercial y movimientos sin picking antes de elegir la fuente del proveedor.
4. La vista hereda `account.view_partner_property_form` y usa permisos `account.group_account_invoice`; deben validarse con la versión Enterprise y roles reales, sin añadir sudo para ocultar errores.
5. No se confirmó que disable_move tenga cero proveedores activos: es un antecedente, no una consulta actual. Su desinstalación histórica tampoco está comprobada aquí.

## Decisión

No incorporar el módulo 14 ni cambiar simplemente False por []: ese cambio corregiría el tipo de retorno pero mantendría la supresión contable sin aprobación funcional. Obtener el uso real de la bandera y el motivo de la excepción; decidir con contabilidad entre flujo estándar y personalización compatible. El código auditado tiene cabeceras AGPL-3, pero no se copió al repositorio ni se ejecutó.

## Pruebas pendientes en copia Odoo 18

| Escenario | Comparaciones |
|---|---|
| Compra→recepción→factura comercial→pago | Recibido/facturado, stock.move y stock.valuation.layer, asientos balanceados y cuentas transitorias. CFDI excluido |
| Coste estándar, AVCO, FIFO según categorías reales | Cantidad/valor/saldos por compañía, redondeos y moneda; no cambiar métodos durante el ensayo |
| Recepción parcial, backorder, devolución proveedor | Cantidades devueltas, valoración vinculada y reversión/asientos correctos |
| Entrega/devolución cliente y POS | Salidas/entradas y coste, ventas/pagos y una sola contabilización |
| Inventario negativo, ajustes, merma y transferencia | Revaloraciones, diferencias justificadas y movimientos internos sin asientos duplicados |
| Multimoneda, fecha de factura distinta, gastos en destino si usados | Diferencias de precio/cambio y capas adicionales conciliadas |
| disable_move activo/inactivo y movimientos sin compra | Comportamiento acordado sin error de tipo ni ausencia indebida de asiento |
| Multiempresa, acceso cajero/compras/contabilidad | Cuentas/compañía correctas y permisos mínimos sin AccessError ni fuga de datos |
| Tablero contable y extractos | Reproducir TestCrawler y balance_end_real con traceback real y roles originales |

Antes/después: cantidades, valoración por producto/compañía/fecha, mayor de inventario, cuentas de entrada/salida, saldos de proveedores/clientes, asientos no balanceados y pagos. Explicar diferencias; ninguna prueba ejecutada todavía. No corregir balances con asientos o SQL manuales durante la auditoría.

Ventas y compras estándar deben probarse de punta a punta con los addons Enterprise y configuraciones reales. No se encontró código propio de sale/purchase en el repositorio actual, lo cual no demuestra ausencia de personalizaciones almacenadas o de Studio.
