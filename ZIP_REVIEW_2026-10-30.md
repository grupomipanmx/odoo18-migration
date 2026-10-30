> Antecedente heredado del repositorio. No se repitieron las pruebas del ZIP en esta sesión; consultar [TEST_REPORT.md](TEST_REPORT.md) y [SOURCE_REVIEW.md](SOURCE_REVIEW.md) para evidencia actual.

# Revisión del ZIP de migración Odoo 18

Fecha: 2026-10-30  
Repositorio destino: grupomipanmx/odoo18-migration  
Archivo revisado: grupomipan-odoo18-migration.zip

## Resultado del inventario

El ZIP contiene 296 entradas. Incluye código fuente de los módulos normales y de dos módulos Softhealer; los directorios de submódulos Git tradicionales están vacíos porque el ZIP del repositorio padre no incorpora el contenido de los gitlinks.

Módulos con fuentes dentro del ZIP:
- `direccion_mx_gmp`
- `disable_trash_pos_order`
- `pos_hide_today_orders`
- `pos_print_group`
- `sh_pos_order_list`
- `sh_pos_order_sync`

Submódulos con directorio vacío en el ZIP: `aspl_pos_order_sync_ee`, `direccion_mx`, `factura_global`, `factura_global_complemento`, `l10n_mx_edi_cancel`, `mass_editing`, `pos_loyalty_fields`, `pos_receipt_client`, `pos_require_product_quantity`, `stock_account_purchase`, `validar_facturas`, `web_m2x_options`.

Se localizaron los repositorios públicos originales de esos submódulos y se consultaron sus manifiestos/árboles. Esto permite continuar la inspección estática sin solicitar otro ZIP. La disponibilidad pública del código no concede derechos adicionales sobre módulos con licencia comercial.

## Hallazgos confirmados en el ZIP

### `sh_pos_order_list`
- Manifiesto: versión 14.0.10, dependencia `point_of_sale`, licencia OPL-1.
- Función declarada: lista de pedidos en POS, consulta de pedidos previos, reordenar y reimprimir.
- El código usa APIs legacy del POS (incluyendo `odoo.define`, `point_of_sale.Registries`, QWeb y assets antiguos).
- No instalar directamente en Odoo 18. Solicitar al proveedor versión 18 o autorización y alcance de actualización.

### `sh_pos_order_sync`
- Manifiesto: versión 14.0.14, depende de `point_of_sale` y `sh_pos_order_list`, licencia OPL-1.
- Función declarada: enviar, recibir, cancelar y cobrar pedidos entre sesiones POS.
- Usa frontend legacy y depende funcionalmente del módulo anterior.
- Deben tratarse como conjunto. No instalar directamente en Odoo 18; solicitar versión compatible al proveedor.

### `direccion_mx_gmp`
- El manifiesto declara versión 18.0.1.0.0, depende de `base` y `contacts`, pero no carga datos, vistas ni seguridad (`data: []`).
- Los modelos conservan nombres técnicos y tablas originales para ciudad, municipio y colonia.
- La extensión de `res.partner` agrega relaciones y onchange, pero no incluye vistas para captura.
- El modelo CP `res.country.state.cp` no declara explícitamente tabla heredada/estructura validada; no asumir compatibilidad con la tabla original sin comparar esquema.
- No está listo para instalar: si el módulo original `direccion_mx` sigue instalado, registrar los mismos nombres de modelo desde otro módulo puede provocar colisión de modelos. Cambiar de nombre técnico de módulo no transfiere automáticamente propiedad de metadatos XML ni resuelve la actualización de esquema.
- Requisito previo: confirmar estado instalado de `direccion_mx`, revisar `ir_model`, `ir_model_fields`, `ir_model_data`, constraints/FKs y tipos de columnas; diseñar transición controlada manteniendo tablas, IDs y referencias. No ejecutar wizard de importación ni reimportar CSV.

### `disable_trash_pos_order`
- Código frontend legacy que extiende TicketScreen y assets antiguos.
- Lógica de negocio: oculta la eliminación para ciertos cajeros y pedidos con pago electrónico completado.
- No portar tal cual; si el control sigue requerido, rediseñarlo con la arquitectura POS 18 y probar permisos, pagos y cancelaciones.

### `pos_hide_today_orders`
- Implementa regla de visibilidad de pedidos y sobrescribe globalmente `ir.rule._eval_context`.
- Esa sobrescritura puede afectar evaluación de reglas fuera de POS.
- No portar tal cual. Si se necesita, implementar una regla limitada al caso POS, sin sustituir globalmente el contexto de seguridad.

### `pos_print_group`
- Extiende configuración POS y frontend legacy para restringir impresión por grupo.
- No instalar directamente. Confirmar que estaba instalado y si la restricción por grupo sigue siendo un requisito.

## Repositorios de submódulos: revisión de manifiestos

- `aspl_pos_order_sync_ee`: módulo POS comercial, cabecera de licencia prohíbe redistribución/modificación; no portar sin autorización.
- `direccion_mx`: versión 14.1; dependencias `base_address_city`, `l10n_mx_edi`, `contacts`; incluye wizard de carga de catálogos. No ejecutar wizard durante migración.
- `factura_global`, `factura_global_complemento`, `l10n_mx_edi_cancel`, `validar_facturas`: personalizaciones CFDI/facturación electrónica, fuera del alcance funcional actual.
- `mass_editing`: versión 14.0.1.0.0, OCA/AGPL-3; validar necesidad antes de portar.
- `pos_loyalty_fields`: versión 14, depende de POS y lealtad; no reinstalar según decisión previa, comprobar referencias huérfanas.
- `pos_receipt_client`: versión 14, POS/Restaurant, plantilla QWeb antigua; validar si el ticket requiere ese dato.
- `pos_require_product_quantity`: versión 14, OCA/AGPL-3; validar si se requiere impedir cantidad cero y adaptar al POS 18.
- `stock_account_purchase`: versión 14; altera comportamiento asociado a `res.partner` y `stock_account`; no reinstalar sin pruebas de valoración/contabilización.
- `web_m2x_options`: versión 14, OCA/AGPL-3; revisar vistas que dependan de sus opciones antes de retirarlo.

## Acciones seguras realizadas

- Inspección local del ZIP y de sus manifiestos/fuentes presentes.
- Identificación de los submódulos Git que el ZIP padre no incluye.
- Localización de repositorios públicos originales y consulta de sus manifiestos y árboles.
- No se modificó la base de datos.
- No se realizó push a Odoo.sh ni se modificó la rama de producción `master`.
- No se declaró ningún módulo como certificado para Odoo 18.

## Pendientes antes de repetir la prueba Upgrade

1. Confirmar en staging el estado real instalado de cada módulo y las dependencias activas.
2. Confirmar con responsables de sucursal qué flujos POS siguen en uso: historial/reorden, sincronización entre sesiones, restricción de impresión, bloqueo de borrado, visibilidad de pedidos y cantidad obligatoria.
3. Para Softhealer/ASPL, obtener versión Odoo 18 o autorización del proveedor; no asumir permiso de modificación.
4. Completar diseño y pruebas de transición de `direccion_mx` preservando tablas, IDs, relaciones y metadatos.
5. Revisar vistas, reglas, acciones, assets y datos que dependan de módulos desinstalados.
6. Validar compras, inventario y contabilidad general con escenarios representativos.
7. Ejecutar pruebas técnicas y funcionales en staging. Producción `master` permanece intacta hasta aprobación expresa.

## Estado

**NO LISTO PARA REPETIR UPGRADE.** El análisis estático avanzó, pero todavía faltan verificaciones en la base staging y pruebas funcionales en Odoo 18.