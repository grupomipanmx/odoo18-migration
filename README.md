# Grupo Mi Pan — Migración a Odoo 18

Repositorio exclusivo para preparar y validar la migración de Odoo 14 a Odoo 18.

## Seguridad
- Trabajar únicamente en staging o copias restaurables.
- No modificar producción ni desplegar sin aceptación.
- No ejecutar SQL destructivo, ni desinstalar módulos sin plan validado.
- No reimportar los CSV de direcciones: las tablas ya contienen registros.
- CFDI/facturación queda fuera del alcance; contabilidad general permanece.

## Direcciones de México
Se portará el módulo conservando el nombre técnico `direccion_mx`, los modelos y las tablas existentes para evitar duplicar datos. No instalar un segundo módulo que registre esos mismos modelos en paralelo.

Conteos reportados en staging Odoo 14: 645 ciudades, 3,060 municipios y 138,035 colonias. La exportación de contactos contiene sólo IDs y campos de dirección; no es un respaldo integral de contactos.

## Flujo
1. Inventario de módulos y dependencias.
2. Portado de módulos propios a Odoo 18.
3. Pruebas en copia de staging.
4. Validación funcional y de datos.
5. Despliegue sólo con aprobación.


## Auditoría y avances
- [Revisión del ZIP y hallazgos técnicos (2026-10-30)](ZIP_REVIEW_2026-10-30.md)
- [Auditoría general de módulos](MODULE_AUDIT.md)

Estado actual: **NO LISTO PARA REPETIR UPGRADE**. El ZIP fue inspeccionado y los hallazgos están documentados. No se ha modificado producción.

- [Brechas técnicas de direccion_mx](DIRECCION_MX_TECHNICAL_GAPS.md)
- [Comprobaciones estáticas del ZIP](STATIC_CHECKS_2026-10-30.md)
