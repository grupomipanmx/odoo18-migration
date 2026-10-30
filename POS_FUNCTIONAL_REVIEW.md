# Revisión funcional POS — 2026-10-30

Estado: revisión estática, port libre de cantidades implementado y propuesta de aceptación. El usuario confirmó sincronización indispensable desde el primer día; cajas independientes NO son alternativa aceptada. **No ejecutado en Odoo 18.** Fuentes y commits: SOURCE_REVIEW.md. Los módulos propietarios se describen desde antecedentes; no se copiaron ni modificaron sus fuentes.

## Matriz de funciones e integraciones

| Función | Evidencia y puntos de integración | Acción |
|---|---|---|
| Historial/recuperación/reimpresión | sh_pos_order_list, OPL-1; según histórico extiende pos.order, filtros de sesión/configuración/días, búsqueda y frontend | Pedir paquete Enterprise 18 y migración de datos/configuración; comprobar historial estándar antes de decidir alcance |
| Sincronización | sh_pos_order_sync, OPL-1; depende de sh_pos_order_list; sesiones emisoras/receptoras, bus, edición/cancelación/pago según histórico | Pedir ambos paquetes compatibles. Identificar dueño del pedido, idempotencia y exclusión de cobro concurrente |
| Motor ASPL | aspl_pos_order_sync_ee, gitlink comercial; uso instalado no confirmado | Pedir versión Enterprise 18 si sigue requerido. No activar dos motores de sincronización por defecto |
| Impresión por grupo | pos_print_group AGPL-3; pos.config.group_print_id, get_cashier/hasGroupPrint, ReceiptScreen.printReceipt | Portar sólo tras fijar identidad empleado/usuario y superficies de impresión. El JS legacy no cubre automáticamente todas las rutas |
| Proteger eliminación | disable_trash_pos_order; hideDeleteButton consulta rol de empleado y pago electrónico done | Sólo protección UI; especificar control servidor para pedidos persistidos, cancelación y pagos. Prever ausencia de empleado |
| Cantidades | pos_require_product_quantity AGPL-3; flag pos.config y _onClickPay legacy | La implementación llama super ANTES de detectar quantity === 0 y no consulta el flag en su JS. Rediseñar antes de pago; no trasladar este orden a 18 |
| Cliente y notas en ticket | pos_receipt_client LGPL-3; plantilla OrderReceipt con receipt.client.name y búsqueda de note por id de línea | Preservar ambos datos si usados; proteger find sin resultado. Revisar payload/export de recibo y pos_restaurant en 18 |
| Visibilidad de pedidos | pos_hide_today_orders LGPL-3, regla y override global ir.rule._eval_context | No reproducir override global. Regla existente permite leer/eliminar sólo fechas anteriores a inicio del día; no es simplemente ocultar un botón |
| Lealtad | pos_loyalty_fields restringe loyalty_points por grupo y frontend readonly | No reinstalar por defecto. Revisar referencias a campos/vistas anteriores y equivalencia con esquema 18 |

## Assets y APIs

Históricos revisados usan imports point_of_sale.Registries, PosModel, ReceiptScreen/ProductScreen/TicketScreen y herencia XML point_of_sale.assets. El manifiesto oficial 18 usa `point_of_sale._assets_pos`; requiere módulos/imports y componentes de la versión destino, carga de datos POS, servicios y contratos de recibo actuales. No basta con cambiar el número de versión o reemplazar cadenas. Se agregó pos_require_product_quantity con dos assets en point_of_sale._assets_pos; se eliminaron de este port los hooks/assets legacy. No se modificó código Softhealer/ASPL.

## Matriz de aceptación futura

Todos los casos están **PENDIENTES**, sin resultados inferidos.

| ID | Caso | Evidencia de aceptación |
|---|---|---|
| POS-01 | Historial por sucursal, compañía, sesión y fecha; cajero vs supervisor | Sólo pedidos autorizados, paginación y límites medidos; sin exposición entre sucursales |
| POS-02 | Recuperar/reordenar y reimprimir pedido antiguo | Distinguir nuevo pedido de reimpresión; no duplicar cobro/asiento; importes, impuestos y descuentos correctos |
| POS-03 | Enviar/recibir/editar/cancelar entre sesiones | Estados coherentes y una sola identidad lógica; trazabilidad de emisor y receptor |
| POS-04 | Pérdida de red, reconexión, reintentos y doble clic | Ningún pedido perdido; deduplicación verificable; sin doble pago |
| POS-05 | Dos cajeros cobran/cancelan el mismo pedido | Un único cobro/contabilización, conflicto controlado y auditoría |
| POS-06 | Impresión manual/automática, reimpresión y cambio de cajero | Grupo autorizado efectivo en cada ruta y sin fuga de permisos tras cambio de empleado |
| POS-07 | Borrado desde interfaz y RPC, con/sin pago autorizado | Protección coherente; cancelación/reembolso definidos; pedidos pagados no eliminados por atajo |
| POS-08 | Cantidad cero, fracciones, unidades, negativa y devolución | Bloqueo antes de pago cuando corresponde; devoluciones legítimas permitidas; validación servidor para pedidos recibidos |
| POS-09 | Cliente, notas, líneas sin nota y pedido reimpreso | Ticket legible y consistente; no error por find indefinido; datos mínimos necesarios |
| POS-10 | Regla de fecha, medianoche, zona México, tz vacío, multiempresa | Visibilidad correcta; no afecta reglas globales; sesiones abiertas y antiguas accesibles según política |
| POS-11 | Venta→pago→stock→cierre→asientos y devolución | Un pedido, pago/stock/asiento conciliables; diferencias de caja explicadas |

Registrar build, usuario/rol, sesión, compañía, pasos, IDs técnicos, logs y resultado esperado/real por caso. Usar datos de ensayo en un destino aislado con correo/pagos/integraciones neutralizados.

## Proveedores

Versiones exactas y preguntas en [SUPPLIER_REQUESTS.md](SUPPLIER_REQUESTS.md). No hay contacto ni autorización comercial confirmada, por tanto no se ha enviado solicitud. Tampoco se ha construido una alternativa a partir de código OPL-1. Las licencias de módulos sin declaración explícita se deben aclarar antes de redistribuirlos.

## Dictamen

**NO APTO para prueba de Upgrade.** Compatibilidad de assets, integridad de sincronización, controles de permisos y aceptación de caja todavía sin pruebas reales.

## Implementación de cantidades 18

El módulo conserva el nombre técnico y el campo pos.config.require_product_quantity. Respeta el flag (False predeterminado como el original), captura el buffer antes de comprobar y bloquea antes de llamar super.pay/validateOrder. El guardia servidor se ejecuta antes del try/except de _process_saved_order del core para no convertir un fallo de validación en un pedido con movimiento de stock. Constraints adicionales cubren state/lines y cambios directos de qty en pedidos finalizados. Borradores pueden contener cero para seguir editándose/sincronizándose; ventas fraccionarias y devoluciones negativas son válidas. No sustituye el motor de sincronización.

11 tests JavaScript con lógica real y dobles explícitos de servicios/base classes pasan en Node; no acreditan OWL, bundle real ni navegador. Cuatro pruebas ORM se prepararon pero no cargan sin Odoo. Historial, impresión, eliminación, cliente/notas y sincronización no están certificados ni se retiraron automáticamente. Ruta y pérdidas temporales en POS_FIRST_UPGRADE.md.
