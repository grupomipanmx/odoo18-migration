# Ruta prioritaria: POS Odoo 18 con sincronización

Fecha: 2026-10-30. **Requisito confirmado por el usuario: sincronización entre sesiones indispensable desde el primer día.** Un POS estándar con cajas independientes no cumple aceptación.

## Solución implementada y límites

1. Port propio direccion_mx 18.0.2.1.0: recupera CP y relaciones, trata textos como datos almacenados y prepara actualización no destructiva. No depende de l10n_mx_edi. La verificación antes/después bloquea pérdidas.
2. Contingencia ejecutable: tools/build_address_bridge.py crea el mismo addon sin sus automatismos, manteniendo todos los modelos y campos. Evita excluir el registro ORM o desinstalar direccion_mx. Pérdidas y recuperación detalladas en DIRECCION_MX_TECHNICAL_GAPS.md. No desplegada ni certificada.
3. Port libre pos_require_product_quantity 18.0.1.0.0: mantiene nombre técnico y flag; dependencias sólo point_of_sale. Reemplaza assets/Registries legacy por bundle e imports 18. Valida antes de pago/confirmación y en servidor; deja borradores editables/sincronizables y admite devoluciones.
4. No se implementó un clon del motor Softhealer/ASPL ni se copiaron sus fuentes. Tampoco se reinstalaron módulos retirados ni se quitaron dependencias de la base sin evidencia. Los dos manifiestos locales no contienen dependencias eliminadas de Odoo 18; el inventario instalado sigue sin verificar.

## Dependencia indispensable todavía externa

Obtener **paquetes oficiales Odoo 18** de sh_pos_order_sync y sh_pos_order_list, con licencia aplicable y procedimiento de migración. Si el motor realmente usado es aspl_pos_order_sync_ee, identificarlo y obtener su versión Enterprise 18; no habilitar dos motores por defecto. Las fichas comerciales no equivalen a código instalado ni prueban compatibilidad entre parches. Solicitudes y referencias en SUPPLIER_REQUESTS.md. No hubo compra, descarga comercial ni envío de correos.

No es viable retirar temporalmente la sincronización porque el usuario lo rechazó. El paquete de cantidades no reemplaza esa función. Historial/reorden, restricción de impresión, protección de eliminación y datos históricos de tickets siguen sujetos a versiones compatibles o port autorizado y pruebas. No se presentan como ya recuperados por esta entrega.

## Secuencia de ensayo, sin producción

1. Obtener runtime 18 Enterprise y PostgreSQL compatibles y paquetes oficiales; identificar versión, licencia y dependencias de cada uno. No reutilizar código 14 de assets/JS por el nombre de carpeta.
2. Instalar en una base vacía desechable los módulos seleccionados y ejecutar los 24 tests ORM. El flag de cantidades se conserva si existía y no se activa masivamente: decidir por configuración POS y probar el efecto sobre pedidos históricos con líneas cero.
3. Capturar respaldo integral, baseline y snapshots de una copia 14; ejecutar flujo oficial de Upgrade en un destino desechable y después scripts del addon. Comparar tablas, IDs, relaciones, textos y contabilidad. No un simple -u sobre una BD 14.
4. Si direccion_mx falla por automatismos de modelo, ensayar el puente conservando los modelos/metadatos. No cambiar tablas ni marcar módulos como desinstalados por SQL. Si falla la prevalidación de datos, detener e inspeccionar; el puente no autoriza saltársela.
5. Probar con dos sesiones y roles reales: enviar/recibir, editar/cancelar, reconectar, repetir entrega, cobrar simultáneamente. Debe existir un solo pedido lógico, un solo cobro y una contabilización conciliable. Confirmar compatibilidad de borradores de cantidad cero y bloqueo antes del pago.
6. Probar ticket, grupos, devoluciones, cierre, stock/asientos, TestCrawler y AccessError previo. Guardar build, comandos, logs e IDs. Ninguno de estos escenarios reales se ejecutó todavía.

## Evidencia actual

12 pruebas Python locales pasan (incluyen SQLite sintético, no PostgreSQL); 11 JavaScript pasan (lógica y patch bodies con dobles explícitos, no OWL). 24 casos ORM preparados sin ejecutar. Compilación, XML y archivos de assets/manifiestos se comprueban estáticamente. No existe evidencia de un build 18 instalado ni de sincronización funcionando. Por tanto: **NO APTO para declarar migración funcional**, aunque el código y las contingencias ya están implementados y publicados.
