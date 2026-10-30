# Requisitos y secuencia de pruebas — Odoo.sh

Fecha: 2026-10-30. **Guía propuesta; no ejecutada.** La captura del usuario muestra Staging → upgrade → 14.0. No acredita base Odoo 18 ni prueba exitosa. El usuario ofrece acceso a SH; se solicitó URL del proyecto/sesión y logs. No enviar contraseñas por chat.

## Acceso y evidencias indispensables

- URL exacta del proyecto Odoo.sh con sesión iniciada y permisos para consultar `upgrade`, builds y logs; identificar repositorio/rama reales asociados. Este repositorio de preparación no se presupone conectado a un build de SH.
- Logs íntegros de Upgrade Odoo 18, carga de módulos, TestCrawler y AccessError; ID de build, versión de código y usuario/grupos. El intento 19 sólo sirve como antecedente, no como destino.
- Estado de módulos instalados/desinstalados y dependientes, vistas Studio y metadatos, y esquema de direccion_mx desde copia autorizada 14. Esta información identifica referencias residuales y posibles pérdidas por limpieza ORM.
- Respaldo integral de BD y filestore con restauración comprobada. La exportación parcial de contactos no sirve para restaurar el ERP.
- Runtime Odoo 18 Enterprise autorizado (community y enterprise de la misma serie/revisión compatible), Python y dependencias según requisitos de esa revisión, PostgreSQL soportado y addons del proveedor versión 18. No usar Python 3.15 local como prueba de compatibilidad.
- Destinos desechables separados: uno vacío para instalar y otro restaurado/migrado para actualizar. No reutilizar ni sobrescribir una base con datos reales de operación.

## Orden de trabajo

1. Consultar sólo builds/logs/configuración en `upgrade`; no cambiar versión, rama ni lanzar instalación por el mero hecho de tener acceso. Confirmar origen 14 y copia recuperable.
2. Capturar referencia de datos/esquema/metadatos de direcciones e inventario/contabilidad y resolver el plan en DIRECCION_MX_TECHNICAL_GAPS. Nada de importaciones CSV ni instalación GMP.
3. Preparar entorno 18 aislado y neutralizado: correo, cron externo, webhooks, pagos, terminales y conexiones con servicios reales deshabilitados para ensayo. Datos de prueba y acceso restringido.
4. Instalar y ejecutar tests sólo en base vacía desechable. Esto prueba el módulo, no la conservación de la base 14.
5. Cuando estén resueltos CP/city/colonia fiscal y metadatos, usar el flujo oficial de Upgrade para convertir una copia 14 a 18; después actualizar código propio en esa copia y comparar integridad. Un `-u` de addon no migra por sí solo una BD de 14 a 18.
6. Ejecutar pruebas POS, ventas, compras, inventario, contabilidad y direcciones; registrar logs/IDs y comparaciones antes/después. Repetir TestCrawler con roles reales.
7. Dictaminar con evidencia; no promover a producción ni tocar master como parte de este trabajo.

## Comandos futuros de referencia (NO ejecutados)

Sólo en un runtime Odoo 18 y un destino comprobado como desechable. Los valores entre `<...>` son marcadores, no comandos listos para copiar. La configuración no debe apuntar a producción. El plan actual aún bloquea actualizar una copia poblada.

```text
python <odoo18>/odoo-bin -c <config_aislada> -d <bd18_vacia_desechable> --addons-path=<core>,<enterprise>,<addons_autorizados> -i direccion_mx --without-demo=all --test-enable --test-tags /direccion_mx --stop-after-init
python <odoo18>/odoo-bin -c <config_aislada> -d <copia_ya_migrada_a_18_desechable> --addons-path=<core>,<enterprise>,<addons_autorizados> -u direccion_mx --test-enable --test-tags /direccion_mx --stop-after-init
```

Guardar versión/commit de todos los addons, comando exacto sin credenciales, salida completa, código de retorno y resumen de tests. No ejecutar scripts de migración 14 de mass_editing ni los wizards de importación de direcciones.

## Criterios para levantar NO APTO

Instalación y actualización sin errores en destino aislado; 24 pruebas ORM ejecutadas; verificación de permisos/vistas; mismos IDs, filas y relaciones de direcciones; funciones POS aceptadas; conciliación inventario/contabilidad sin diferencias injustificadas; errores TestCrawler y AccessError resueltos con trazabilidad. La producción requiere una aprobación posterior independiente.

## Acceso ofrecido durante esta sesión

El usuario compartió la URL https://www.odoo.sh/project/grupomipan y confirmó haber iniciado sesión. El inventario de ventanas mostró Chrome en «Odoo.sh - grupomipan - Branches». Al intentar observar la página, el control del navegador se detuvo porque no pudo verificar con suficiente confianza la URL activa de Chrome. No se consultaron builds ni logs, ni se ejecutaron cambios en SH. El acceso autenticado y la revisión del staging quedan pendientes de verificación por una herramienta operativa.

No se guardaron credenciales, capturas ni claves SSH en el repositorio. La clave pública por sí sola no proporciona autenticación SSH; no se solicitó clave privada. La guía de control de Windows exige que los diálogos de autenticación los complete el usuario.

## Seguimiento implementado: POS primero

Ver POS_FIRST_UPGRADE.md. El usuario no acepta cajas sin sincronización. Los paquetes comerciales 18 son requisito, no se retiran para obtener una carga aparente. Agregar pos_require_product_quantity al ensayo desechable y ejecutar tests de ambos addons; su flag es configurable y no se activa masivamente. Los scripts pre/post de direccion_mx están preparados y aún no se han ejecutado en Odoo; generar/cotejar snapshots antes y después. No guardar snapshots ni copias de datos reales en Git.

El puente generado por tools/build_address_bridge.py sólo sustituye temporalmente el código del mismo direccion_mx en una copia aislada. No desinstala modelos ni importa catálogos. Es una herramienta de ensayo, no una autorización de despliegue o una garantía de instalación.
