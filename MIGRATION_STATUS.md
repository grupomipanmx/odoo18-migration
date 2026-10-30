# Estado técnico

- Repositorio de trabajo: grupomipanmx/odoo18-migration
- Rama: main
- Acceso de escritura verificado.
- Base de referencia: Odoo 14; objetivo Odoo 18.
- Producción no se modifica.

## Direcciones México
Conservar nombre técnico `direccion_mx`, modelos y tablas:
- res_country_state_ciudad (645 registros reportados)
- res_country_state_municipio (3,060)
- res_country_state_municipio_colonia (138,035)

Campos de contacto existentes: ciudad_id, municipio_id, colonia_id, l10n_mx_edi_colony. Mantener IDs y relaciones.

## Restricciones
No instalar el módulo portado en paralelo con el legado; no desinstalar el legado; no reimportar CSV; no ejecutar el asistente antiguo de post-instalación ni el importador CSV antiguo. La exportación contactos_direcciones.csv sólo contiene IDs y campos de dirección, no todos los datos de res_partner.

## Riesgos
El módulo legado depende de l10n_mx_edi y contiene vistas/APIs antiguas. La versión Odoo 18 elimina esa dependencia de catálogos; CFDI queda fuera del alcance. La transición debe probarse en una copia restaurable y validar conteos, IDs y relaciones antes/después.
