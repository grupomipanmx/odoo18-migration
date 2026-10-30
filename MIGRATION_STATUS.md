# Estado de migración — 2026-10-30

**NO APTO para prueba de Upgrade.** Preparación parcial documentada; no migración certificada.

Repositorio: `grupomipanmx/odoo18-migration`. Rama: `codex/odoo18-compatibility`. Base: `318677df86c611d16bf54c0c59869a5c1a901934`. Trabajo local aislado de ERP_JM_LITE. Destino Odoo 18 Enterprise; Odoo 19 no forma parte del trabajo.

| Fase | Resultado verificable | Pendiente |
|---|---|---|
| Auditoría | Todos los archivos del repositorio leídos; fuentes históricas autorizadas, manifiestos y 12 gitlinks revisados | Estado instalado y referencias almacenadas en BD, fuentes comerciales 18 autorizadas |
| Direcciones | CP restaurado, textos almacenados, normalización API y scripts pre/post preparados; comparador y puente temporal implementados | Ejecución PostgreSQL/Odoo, esquema real, metadatos/XML IDs y comparación de snapshots |
| POS | Port libre de cantidades con controles antes de pago y servidor; sincronización confirmada indispensable desde día uno | Paquetes oficiales de sincronización 18 y prueba real de concurrencia/cobro |
| Inventario/contabilidad | Identificada supresión de asientos y contrato de retorno incompatible | Decisión contable y conciliación real |
| Implementación | direccion_mx 18.0.2.1.0, pos_require_product_quantity 18.0.1.0.0 y contingencia empaquetable | No instalados ni desplegados; resto de extensiones según necesidad real |
| Pruebas | 12 pruebas Python locales y 11 JS pasan; sintaxis/XML/manifiestos/ACL/assets locales pasan | 24 pruebas ORM sin ejecutar por ausencia de odoo; instalación/actualización no ejecutadas |
| Documentación | Archivos de entrega actualizados, evidencias y requisitos preparados | Evidencia staging y aceptación funcional |

## Decisiones y riesgos

- D01: conservar `direccion_mx` como único propietario técnico. No instalar GMP ni copiar modelos simultáneos. El mismo nombre no garantiza preservar XML IDs antiguos.
- D02 (actualizada): el usuario autorizó corregir CP y textos y preparar ruta POS. Se recupera el modelo CP sin índices/requisitos nuevos; city/colonia fiscal son textos almacenados. Se incluyen prevalidación y backfill NULL-only para ensayo futuro; no se ejecutó SQL en una BD Odoo ni se tocaron datos reales.
- D03: no incorporar ni modificar Softhealer/ASPL. [Solicitud pendiente](SUPPLIER_REQUESTS.md); no se envió comunicación a terceros.
- D04: no portar la supresión contable de `stock_account_purchase` sin definición funcional y conciliación. No se eliminó el campo histórico `disable_move` de ninguna BD.
- D05: no reinstalar módulos reportados como retirados. Su estado real debe verificarse en `ir.module.module` y con los responsables.
- D06: no dar por resueltos los errores TestCrawler/AccessError por nombre de campo. Se requiere traceback íntegro, usuario/grupos, versión/build y módulo responsable.
- D07: el usuario ofrece acceso a Odoo.sh; la captura muestra `upgrade` 14.0. El usuario confirmó sesión iniciada y compartió la URL del proyecto. La observación de Chrome se detuvo por no poder verificar su URL activa; no se leyeron logs ni se lanzó build/Upgrade. Siguen pendientes logs y respaldo restaurable.

- D08: sincronización obligatoria desde día uno, confirmada por el usuario. No se acepta retirar Softhealer/ASPL y llamar funcional a un POS independiente. No se desarrolló ni copió un sustituto propietario.
- D09: puente temporal empaquetable conserva nombre/modelos/campos/vistas/ACL; excluye automatismos de dirección, no sus registros. No fue desplegado. Su recuperación restaura el addon completo en la misma ruta y exige comparar snapshots.
- D10: no se retiró ninguna dependencia instalada sin inventario/traceback. Los manifiestos actuales sólo dependen de base/contacts y point_of_sale compatibles con 18; pos_require_product_quantity ya no usa assets/Registries legacy.

## Bloqueos concretos y cierre

1. Acceso de lectura al proyecto Odoo.sh y logs completos del intento 18, TestCrawler `account.menu_board_journal_1` y AccessError `account.bank.statement.last_statement_id.balance_end_real`. Permiten asignar causas sin inventar correcciones.
2. Inventario real de módulos y exportación de esquema/metadatos/direcciones desde copia autorizada 14; respaldo integral + filestore con restauración comprobada. Permiten diseñar conservación verificable.
3. Base desechable Odoo 18 Enterprise con addons autorizados, dependencias y PostgreSQL. Permite ejecutar las 24 pruebas ORM, instalar en vacío y actualizar una copia migrada.
4. Paquetes 18 de Softhealer/ASPL y soporte de migración confirmado, según módulos realmente usados.
5. Aceptación operativa de ventas, pagos, compras, valoración y contabilidad. No hay resultados funcionales todavía.

La falta de estos recursos no impidió completar la auditoría local ni la corrección acotada. Los pasos de instalación sobre datos poblados siguen condicionados a revisar el plan y comprobar un destino desechable.

## Evidencia

[TEST_REPORT.md](TEST_REPORT.md), [SOURCE_REVIEW.md](SOURCE_REVIEW.md), [STAGING_RUNBOOK.md](STAGING_RUNBOOK.md). No hubo conexión a BD Odoo, importación CSV, despliegue ni modificación de producción. Las pruebas SQL locales usaron exclusivamente SQLite en memoria con fixtures sintéticos.
