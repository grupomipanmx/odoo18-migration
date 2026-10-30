# Grupo Mi Pan — Migración Odoo 14 → Odoo 18 Enterprise

**Dictamen al 2026-10-30: NO APTO para prueba de Upgrade.** Se preparó una corrección de compatibilidad; no hay evidencia de instalación, actualización ni aceptación funcional en Odoo 18 Enterprise.

Rama de trabajo: `codex/odoo18-compatibility`, desde `main` commit `318677df86c611d16bf54c0c59869a5c1a901934`. No se modifican `main`, `master`, producción ni bases de datos. No hay despliegue autorizado como parte de esta entrega.

## Alcance

Ventas, POS, compras, inventario, contabilidad general y catálogos mexicanos. HR, CFDI, factura global y validaciones fiscales quedan fuera del alcance funcional; sus dependencias técnicas deben resolverse sin desinstalaciones automáticas.

## Entrega actual

- Auditoría de todos los archivos del repositorio y revisión autenticada de fuentes históricas y submódulos: [MODULE_AUDIT.md](MODULE_AUDIT.md), [SOURCE_REVIEW.md](SOURCE_REVIEW.md).
- Corrección en `direccion_mx`: búsqueda por nombre/CP mediante `_search_display_name` de Odoo 18. Se preservan filtros del llamador, reglas de registros y semántica de operadores negativos. Sin cambios en declaraciones de campos, tablas o manifiesto.
- Siete pruebas Odoo de regresión preparadas, pendientes de ejecución con un servidor real.
- [Plan de conservación de direcciones](DIRECCION_MX_TECHNICAL_GAPS.md), [revisión POS](POS_FUNCTIONAL_REVIEW.md), [inventario y contabilidad](STOCK_ACCOUNT_REVIEW.md).
- [Resultados reales](TEST_REPORT.md), [requisitos de entorno](STAGING_RUNBOOK.md), [versiones a solicitar al proveedor](SUPPLIER_REQUESTS.md), [estado y decisiones](MIGRATION_STATUS.md).

## Verificación local reproducible

```powershell
python tools/check_repository.py
python -m compileall -q direccion_mx tools
git diff --check
```

Estas comprobaciones no importan el ORM ni validan instalación. El entorno local tiene Python 3.15.0 y carece de Odoo, psycopg2, lxml y ejecutables PostgreSQL/Docker detectables. No se ha preparado un runtime Odoo compatible.

## Preservación de datos

Usar un solo módulo técnico `direccion_mx`. No instalar `direccion_mx_gmp` en paralelo, reimportar CSV, desinstalar el legado, ejecutar wizards antiguos o eliminar/recrear tablas. Los conteos históricos (645 ciudades, 3,060 municipios, 138,035 colonias) no fueron medidos en esta sesión.

**No ejecutar instalación/actualización sobre la base poblada hasta revisar el plan de esquema y sus riesgos.** Que el manifiesto existente declare `installable=True` no equivale a aprobación técnica.

## Antecedentes

[ZIP_REVIEW_2026-10-30.md](ZIP_REVIEW_2026-10-30.md) y [STATIC_CHECKS_2026-10-30.md](STATIC_CHECKS_2026-10-30.md) son reportes heredados. Sus resultados no se presentan como pruebas repetidas en esta sesión. El contexto adjunto del usuario confirma intentos fallidos 18/19 y prioriza exclusivamente Odoo 18. La captura recibida muestra el staging `upgrade` en 14.0; no demuestra un build Odoo 18 funcional.
