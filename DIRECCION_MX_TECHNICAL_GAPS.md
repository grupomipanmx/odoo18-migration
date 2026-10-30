# Direcciones mexicanas — implementación y conservación

Fecha: 2026-10-30. Versión implementada: **18.0.2.1.0**. Código publicado en codex/odoo18-compatibility. **No instalado ni actualizado en Odoo; conservación de datos reales todavía no demostrada.**

## Brechas corregidas en código

| Elemento | Implementación |
|---|---|
| CP | Modelo res.country.state.cp y tabla explícita res_country_state_cp. name Char tamaño 128, state_id, ciudad_id y municipio_id opcionales, mismos destinos que legado. Sin importación, índices nuevos, restricciones nuevas ni recreación de tabla |
| city | Char almacenado/editable estándar, sin related/compute/inverse. Compatible con texto libre y contactos sin catálogos mexicanos |
| l10n_mx_edi_colony | Char almacenado/editable con el mismo nombre, sin dependencia CFDI. No se descarta texto fiscal original |
| Alta/edición por API | create multi y write completan únicamente valores omitidos al seleccionar explícitamente ciudad/municipio/colonia. El texto explícito, incluso vacío, prevalece |
| Coherencia | Nuevas selecciones contradictorias producen ValidationError antes de reemplazar relaciones. No se normalizan masivamente contactos históricos |
| Contactos hijos | _address_fields incorpora relaciones y colonia fiscal para que el mecanismo estándar sincronice dirección y vínculos juntos |
| Seguridad CP | Internos lectura; sistema CRUD, igual a otros catálogos. ACL aditivas: comprobar permisos heredados en la copia real |
| Búsqueda | Se conserva la corrección _search_display_name de la entrega anterior |

Un cambio de teléfono o de otro dato ajeno a los selectores no reescribe las direcciones. Limpiar todos los selectores conserva el texto guardado; renombrar un catálogo tampoco reescribe las etiquetas históricas de los contactos. Elegir una nueva colonia por formulario sí actualiza las etiquetas mediante onchange. Esta es una decisión explícita de transición a textos estándar, no una equivalencia exacta del related legado.

El legado mostraba city/colonia a través de related no almacenados. Si las columnas guardadas y el texto efectivo del related ya difieren, el port prioriza los textos almacenados: el comparador de snapshots debe señalar la diferencia y bloquear aceptación hasta una decisión documentada. No se intenta resolverla sobrescribiendo masivamente los datos. Si l10n_mx_edi u otro addon redefine estos campos, debe comprobarse su definición final en el registry Enterprise; no se modificó código propietario.

## Scripts de actualización preparados, no ejecutados en Odoo

- migrations/18.0.2.1.0/pre-migrate.py: valida tablas/columnas originales y referencias no huérfanas. Un esquema inesperado, CP ausente o referencias rotas bloquean el ensayo; nunca se corrigen borrando ni recreando registros.
- post-migrate.py: rellena city y l10n_mx_edi_colony **sólo si son SQL NULL** y existe el registro relacionado. Conserva textos no nulos, cadenas vacías, IDs y relaciones. No importa CSV, no elimina registros y no altera tablas. Su lógica pasó tres pruebas con fixtures sintéticos SQLite en memoria; no es validación PostgreSQL/Odoo.
- El ORM podrá materializar la columna fiscal al actualizar: declarar un campo almacenado también puede generar DDL. Este cambio de esquema está preparado en código, no se ha aplicado a ninguna base real.
- El salto 14→18 requiere el servicio/proceso oficial de Upgrade. Estos scripts de addon no reemplazan la migración del core.

## Comprobación de conservación

`tools/address_integrity.py` ofrece snapshot(env) en lectura ORM y comparación offline. Incluye los cuatro catálogos y todos los partners, también archivados y proveedores si supplier_rank existe. Lee por lotes y conserva hashes por ID de nombres, textos y relaciones, además de los nombres de tablas y cobertura de campos; no exporta nombres de personas en claro. Las lecturas deben ejecutarse en una copia autorizada, con una transacción de lectura consistente y sin cambios concurrentes. No se ejecutaron aquí sobre Odoo.

Capturar antes del Upgrade, bajo el registro 14, y después bajo 18. Guardar fuera de Git y comparar:

```text
python tools/address_integrity.py <antes.json> <despues.json>
```

El comparador falla ante modelos faltantes, campos incompletos, cambio de tabla, IDs agregados/eliminados o hashes distintos. Revisar también FKs, tipos/nullability/defaults/índices/secuencias, XML IDs/noupdate y propiedad de ir.model/ir.model.fields. Las comprobaciones de snapshots no sustituyen esa auditoría de esquema/metadatos. Incluso nuevos partners legítimos del core producen una diferencia que debe revisarse; no existe una excepción automática que oculte pérdidas.

La conservación se acepta sólo con snapshots reales comparables, logs sin limpieza imprevista y esquema verificado. No es posible garantizarla sobre una BD no inspeccionada; las salvaguardas implementadas evitan declarar éxito sólo por conteos.

## Contingencia temporal implementada

```text
python tools/build_address_bridge.py <archivo_nuevo.zip>
```

Genera una variante del **mismo direccion_mx** con los cuatro modelos/campos y sus tablas. Conserva manifiesto, vistas, ACL y scripts para no retirar metadatos XML por quitar archivos de data. Elimina únicamente métodos personalizados de los modelos. No conecta a BD y rechaza sobrescribir el archivo de salida.

Se pierde temporalmente: búsqueda de colonia por CP, onchanges, autocompletado por API, validación de coherencia y extensión de sincronización de direcciones con hijos. Los selectores quedan manuales; no usar este paquete para operación real. No se retiran los modelos, no se desinstala el módulo, no se instala GMP y no se cambia ningún ID. Mantener un solo ejemplar en addons_path.

Recuperación: restaurar el addon completo 18.0.2.1.0 en la misma ruta, reiniciar y ensayar la actualización únicamente en copia desechable; volver a comparar snapshots. El puente no remedia un esquema corrupto ni evita la prevalidación; ante un fallo hay que inspeccionar/restaurar otra copia. Tres pruebas de empaquetado verifican declaraciones idénticas y ausencia de sobrescritura. No hay prueba de instalación del puente en Odoo.

## Pruebas y límites

20 casos ORM de direcciones preparados: siete búsquedas originales y 13 nuevos para CP, campos, textos, API, contactos/proveedores archivados, relaciones/IDs, lotes, conflictos, hijos y ACL. No ejecutados por ausencia de Odoo. Comparador, empaquetado y backfill tienen 12 pruebas Python locales aprobadas en total. Evidencia completa en TEST_REPORT.md.

Conteos históricos: 645 ciudades, 3,060 municipios y 138,035 colonias; no medidos aquí. No se tocó producción, main/master ni bases reales. Fuentes y commits originales en SOURCE_REVIEW.md. **NO APTO para Upgrade funcional hasta probar conservación en una copia Odoo 18 y la sincronización POS obligatoria.**
