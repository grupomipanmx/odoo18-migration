# Versiones a solicitar a proveedores

Fecha: 2026-10-30. **Borradores preparados; solicitudes NO enviadas.** El usuario no tiene contacto ni autorización comercial confirmados. No se copió, redistribuyó ni modificó código Softhealer/ASPL.

## Softhealer

Solicitar versiones **Odoo 18 Enterprise** de `sh_pos_order_list` y `sh_pos_order_sync`, compatibles entre sí, y servicio/guía de migración desde 14.0.10 y 14.0.14 respectivamente (versiones históricas reportadas).

Texto para enviar cuando exista contacto confirmado:

> Grupo Mi Pan migra Odoo 14 Enterprise a Odoo 18 Enterprise en Odoo.sh. Necesitamos confirmar disponibilidad, licencia de uso en staging/producción, coste y soporte de las versiones 18 de sh_pos_order_list y sh_pos_order_sync. Solicitamos paquetes oficiales, manifiestos y dependencias, instrucciones para conservar pedidos/configuraciones y migración soportada de 14 a 18. Confirmen historial, recuperación/reorden y reimpresión, sincronización entre sesiones, roles, bus, desconexión/reintentos, cancelaciones y protección de cobro concurrente. Indiquen diferencias funcionales, limitaciones multiempresa/sucursal, mecanismos de idempotencia y pruebas de aceptación recomendadas.

## ASPL / proveedor identificado por el contrato

Solicitar **Odoo 18 Enterprise** de `aspl_pos_order_sync_ee`, si se confirma su uso actual. La titularidad/contacto no se da por verificada sólo por el nombre del módulo.

Texto preparado:

> Grupo Mi Pan requiere confirmar titular y soporte de aspl_pos_order_sync_ee y disponer de versión oficial para Odoo 18 Enterprise/Odoo.sh. Solicitamos términos de licencia, cobertura de staging, dependencias y procedimiento de migración de datos/configuración desde 14, soporte de sincronización, concurrencia, reconexión y pagos. Confirmen compatibilidad o exclusión con Softhealer sh_pos_order_list/sh_pos_order_sync y cambios de comportamiento.

## Entregables necesarios del proveedor

Paquetes 18 oficiales con versiones identificables; condiciones de licencia y autorización de uso; dependencias compatibles; instrucciones de actualización de datos; limitaciones conocidas; soporte para ensayo y errores. No desarrollar un sustituto copiando su implementación. No instalar dos motores de sincronización sin diseño validado.
