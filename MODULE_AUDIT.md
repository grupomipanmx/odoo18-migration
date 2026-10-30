# Auditoría de módulos — Migración Odoo 14 a Odoo 18

Fecha de revisión: 2026-10-30  
Repositorio de trabajo: grupomipanmx/odoo18-migration  
Entorno de validación: rama Odoo.sh `upgrade`  
Producción `master`: no modificar.

## Alcance acordado
- Mantener ventas, Punto de Venta, compras, inventario y contabilidad general.
- Recursos Humanos queda fuera del alcance.
- CFDI, facturación electrónica mexicana y módulos de factura global quedan fuera del alcance.
- Conservar los catálogos de direcciones de México y sus relaciones con contactos.
- No desinstalar módulos adicionales ni ejecutar cambios destructivos sin validar dependencias y datos.

## Estado según el historial de pruebas y cambios reportados

| Módulo técnico | Estado conocido | Acción para Odoo 18 | Observaciones |
|---|---|---|---|
| `direccion_mx` | Instalado en Odoo 14; se acordó conservarlo | PORTAR Y VALIDAR | Mantener modelos, tablas, IDs y relaciones existentes. No instalar una segunda copia en paralelo ni reimportar CSV. |
| `mass_editing` | Desinstalado en staging | VALIDAR NECESIDAD | No reinstalar sin confirmar si existe una alternativa estándar o si se usa en procesos actuales. |
| `web_m2x_options` | Desinstalado en staging | VALIDAR VISTAS/DEPENDENCIAS | Revisar vistas personalizadas que usaran sus opciones antes de decidir sustitución. |
| `disable_trash_pos_order` | Desinstalado en staging | REVISAR POS | Confirmar si el bloqueo de eliminación de pedidos es un control operativo requerido y reemplazarlo si aplica. |
| `pos_hide_today_orders` | Desinstalado en staging | REVISAR POS | Confirmar si ocultar pedidos del día era parte del flujo de caja. |
| `pos_require_product_quantity` | Desinstalado en staging | REVISAR POS | Confirmar si se requiere impedir líneas de producto con cantidad no capturada/cero. |
| `pos_receipt_client` | Desinstalado en staging | REVISAR POS | Confirmar si el ticket requiere mostrar datos adicionales del cliente. |
| `pos_loyalty_fields` | Desinstalado en staging | REVISAR POS/LEALTAD | Se reportó que se conserva `pos_loyalty`; comprobar que no haya campos/vistas dependientes del módulo retirado. |
| `stock_account_purchase` | Desinstalado en staging | REVISAR INVENTARIO/CONTABILIDAD | Se reportó que `res.partner.disable_move` no tenía registros activos; comprobar el flujo contable de compras y valoración antes de darlo por sustituido. |
| `factura_global` | Estado final no confirmado | FUERA DE ALCANCE | No migrar ni reinstalar en esta fase; confirmar que no bloquee la carga de módulos dentro del alcance. |
| `factura_global_complemento` | Estado final no confirmado | FUERA DE ALCANCE | Relacionado con factura global/CFDI. |
| `validar_facturas` | Estado final no confirmado | FUERA DE ALCANCE | Relacionado con validaciones de facturación. |

## Errores detectados en el intento anterior
- Módulos reportados como inconsistentes: `direccion_mx`, `disable_trash_pos_order`, `factura_global`, `factura_global_complemento`, `mass_editing`, `pos_hide_today_orders`, `pos_loyalty_fields`, `pos_receipt_client`, `pos_require_product_quantity`, `stock_account_purchase`, `validar_facturas`, `web_m2x_options`.
- Se reportaron errores de vistas XML (incluyendo indentación inesperada) y fallos del TestCrawler en el tablero de contabilidad (`account.menu_board_journal_1`).
- También se reportó un AccessError relacionado con `account.bank.statement.last_statement_id.balance_end_real`; requiere analizar el traceback completo y el módulo responsable antes de corregir.
- Los errores HR se excluyen conforme al alcance acordado.

## Pendiente para cerrar la auditoría de código
El repositorio de migración contiene actualmente el port inicial de `direccion_mx`, pero no contiene los fuentes de los otros módulos personalizados retirados ni los módulos de facturación. Por eso, su clasificación anterior se basa en el historial de la prueba y en los nombres/funciones reportados, no en una inspección línea por línea de sus fuentes.

Para revisar código de cada módulo se necesita que su carpeta fuente esté disponible en este repositorio o en un archivo exportado. No se debe asumir que el nombre del módulo describe todas sus personalizaciones.

## Criterios de aceptación antes de repetir Upgrade
1. Cada módulo dentro del alcance tiene versión Odoo 18 compatible o una sustitución funcional aprobada.
2. No quedan dependencias de módulos retirados en vistas, acciones, reglas, campos, datos XML ni manifiestos.
3. Las funciones POS, compras, inventario y contabilidad general se prueban con escenarios reales.
4. Los catálogos de dirección conservan conteos, IDs y relaciones; no se ejecuta una importación duplicada.
5. La prueba se realiza únicamente en `upgrade`; `master` permanece intacta hasta aprobación expresa.


## Hallazgos adicionales al inspeccionar fuentes POS originales
Se inspeccionaron fuentes disponibles en el repositorio histórico `jeffrepo/grupomipan`, rama `odoo18-migration`:

### `disable_trash_pos_order`
- El módulo modifica el POS frontend con la API legacy `odoo.define`, `point_of_sale.Registries` y `TicketScreen`.
- La lógica oculta el botón de borrar para cajeros y para pedidos con pagos electrónicos completados.
- Su XML hereda `point_of_sale.assets`, patrón de assets antiguo.
- Conclusión: no es compatible para copiar directamente a Odoo 18. Si el negocio requiere impedir borrado de pedidos, hay que rediseñar el control con el framework POS de Odoo 18 y probar permisos/roles. No reinstalar el módulo 14.

### `pos_hide_today_orders`
- Implementa una regla de registros sobre `pos.order` para ocultar pedidos del día a un grupo.
- Sobrescribe `ir.rule._eval_context`, lo que puede afectar el contexto de evaluación de otras reglas, no sólo la regla del POS.
- Usa `user.login_date.now(...)` y el módulo de seguridad tiene un dominio de fecha que requiere revisión.
- Conclusión: no portar tal cual. Confirmar qué usuarios pertenecen al grupo y qué problema operativo resuelve; si sigue requerido, sustituirlo por una regla limitada al caso POS sin reemplazar globalmente el contexto de `ir.rule`.

### `pos_print_group` (presente en el código histórico; no figura en la lista previa de módulos desinstalados)
- Añade un grupo de seguridad para permitir imprimir tickets.
- Extiende `pos.config` con `group_print_id` y modifica `ReceiptScreen`/cajero mediante APIs legacy del POS.
- El manifest depende de `point_of_sale` y carga assets por `point_of_sale.assets`.
- Conclusión: requiere confirmar si estaba instalado y si el bloqueo de impresión por grupo sigue siendo requisito. Si se conserva, reimplementar con los assets/componentes de POS de Odoo 18. No se debe asumir que está desinstalado.

## Limitación de esta auditoría
Los módulos `pos_require_product_quantity`, `pos_receipt_client`, `pos_loyalty_fields`, `stock_account_purchase`, `web_m2x_options` y `mass_editing` aparecen como submódulos Git (gitlinks) en el repositorio histórico. Sus fuentes no están disponibles como archivos normales en el árbol principal inspeccionado; se requiere acceder a cada repositorio de submódulo o recibir un ZIP/exportación para revisar el código completo. Los módulos de factura global también son submódulos y permanecen fuera del alcance funcional acordado.

## Estado de preparación
**NO LISTO PARA REPETIR UPGRADE.** Faltan fuentes y validaciones técnicas de los módulos indicados, además de terminar la validación de `direccion_mx`. Esta marca evita confundir una auditoría parcial con una aprobación de migración.
