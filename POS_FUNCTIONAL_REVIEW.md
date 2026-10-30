# Revisión funcional de extensiones POS

Fecha: 2026-10-30  
Fuente: módulos incluidos en el ZIP del usuario.

## Flujos identificados

### Historial de pedidos — sh_pos_order_list
El README del proveedor y el código indican que agrega una lista de pedidos en la pantalla POS. Permite consultar pedidos anteriores, reordenar y reimprimir sin cerrar la sesión. En el backend agrega campos a pos.order y métodos de búsqueda/lectura; agrega filtros por sesión, días y configuración POS. Su código frontend usa el framework POS anterior a OWL moderno.

Riesgos:
- Permisos y alcance de búsqueda: los métodos consultan pedidos según usuario, configuración, sesión y filtros; deben probarse con cajeros de distintas sucursales para evitar exposición cruzada de pedidos.
- Volumen: el modo de consulta de todas las sesiones/pedidos puede cargar conjuntos amplios; revisar paginación y límites.
- Compatibilidad: frontend, QWeb, RPC y assets son legacy.
- Licencia OPL-1. No copiar/modificar sin autorización.

### Sincronización entre sesiones — sh_pos_order_sync
El README describe un flujo de captura/envío, recepción, edición, cancelación y cobro de pedidos en otras sesiones POS. El manifiesto depende de sh_pos_order_list. El código agrega campos de configuración para tipo de usuario (envía/recibe/ambos), permiso de pago, edición, cancelación y selección múltiple; usa notificaciones del bus.

Escenarios que deberá cubrir una prueba funcional:
1. Capturar pedido en POS emisor y enviarlo al POS receptor.
2. Recibirlo sin duplicarlo.
3. Modificar líneas y confirmar que los cambios se reflejan en ambas sesiones.
4. Cancelar y verificar la notificación/estado en las sesiones involucradas.
5. Cobrar desde el POS autorizado y confirmar un único pedido/una única contabilización.
6. Simular desconexión/reconexión y evitar pérdida o duplicidad.
7. Probar concurrencia: dos usuarios intentando cobrar o cancelar el mismo pedido.
8. Probar permisos: emisor, receptor, usuario de sólo consulta y cajero.

No se puede garantizar integridad de pedidos sólo porque el módulo cargue. El flujo requiere pruebas de concurrencia, bus, estados y pagos.

### Restricción de impresión — pos_print_group
Agrega un grupo de seguridad y transmite al frontend si el cajero pertenece al grupo. La extensión de ReceiptScreen sólo imprime cuando el usuario tiene el grupo. El código utiliza odoo.define, point_of_sale.Registries y point_of_sale.models, incompatibles para uso directo en el POS moderno.

### Protección de eliminación — disable_trash_pos_order
Oculta el botón de borrar para determinados cajeros y pedidos con pago electrónico completado. Esto es una protección de interfaz, no debe considerarse por sí sola un control de seguridad de backend. Si se conserva, validar también las rutas backend/RPC y el tratamiento de pagos ya autorizados.

### Ocultar pedidos del día — pos_hide_today_orders
La personalización altera el contexto global de evaluación de reglas ir.rule. No se debe reproducir ese override. Si el objetivo es limitar qué pedidos ve cada grupo, diseñar una regla de registros específica, con dominios y pruebas multiempresa/sucursal, sin cambiar el contexto global.

## Código de terceros y licencias
- sh_pos_order_list y sh_pos_order_sync declaran licencia OPL-1 y datos del proveedor Softhealer.
- No se recomienda crear un fork modificado ni distribuir el código en un módulo nuevo sin revisar contrato/licencia y obtener autorización escrita.
- Alternativa preferente: pedir al proveedor versión compatible con Odoo 18 y cotización/soporte de migración. Si no existe, especificar funcionalidad equivalente desde cero con implementación propia, sin copiar código propietario.

## Criterio de decisión
No seleccionar una implementación técnica hasta confirmar qué flujos se usan realmente en sucursales. La decisión debe basarse en el proceso operativo, no sólo en que el módulo figure en el repositorio histórico.

## Estado
Revisión estática funcional completada para los módulos POS incluidos en el ZIP. No se ejecutaron en Odoo 18 ni se confirmó su estado instalado en la base staging. Por tanto, no se certifica compatibilidad ni se autoriza repetir Upgrade.
