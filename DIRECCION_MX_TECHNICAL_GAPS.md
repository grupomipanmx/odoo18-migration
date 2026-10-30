# Direcciones mexicanas: propuesta técnica y riesgos

Fecha: 2026-10-30. **Plan presentado; ningún cambio de esquema ni operación de BD ejecutado. NO APTO para instalar/actualizar sobre base poblada.**

## Comparación confirmada

| Elemento | Legado direccion_mx | GMP histórico | Port actual |
|---|---|---|---|
| Identidad | direccion_mx | direccion_mx_gmp | direccion_mx |
| Dependencias | base_address_city, l10n_mx_edi, contacts | base, contacts | base, contacts |
| Modelos catálogos | Ciudad/municipio/colonia y CP | Los cuatro | Sólo los primeros tres; CP falta |
| Tablas principales | Nombres derivados originales | Nombres explícitos conservados | Nombres explícitos conservados |
| Interfaz/ACL | Vistas/wizards; init_xml antiguo | Sin data | ACL + vistas cargadas |
| city | Related a ciudad_id.name | Asignación onchange | Asignación onchange; puede divergir por RPC/import |
| l10n_mx_edi_colony | Related a colonia_id.name | Ausente | Related readonly, store no declarado |
| Búsqueda colonia | name_search + name_get | name_search + name_get | _name_search inefectivo en 18; corregido al dominio display_name |

Las brechas del GMP sin vistas/ACL son históricas, no describen el port actual. Recuperar un archivo de modelo no resuelve por sí solo la transición de metadatos ni el esquema.

## Estrategia de conservación

1. **Inventario en lectura desde copia autorizada 14.** Confirmar ir.module.module y dependientes; verificar si GMP se instaló alguna vez. Obtener definiciones de modelos/campos, módulos propietarios de metadatos y todos los XML IDs/vistas/acciones/reglas. No instalar ambos ni desinstalar el legado para resolver conflictos.
2. **Respaldo integral y referencia.** Base completa + filestore, versión de código y addons; restauración comprobada. Registrar conteos reales, IDs ordenados y huellas por fila de cada catálogo, más referencias de todos los contactos (activos/archivados, clientes/proveedores, hijos, empresas). La exportación parcial de contactos no basta.
3. **Esquema antes de tocarlo.** Comparar tipos, longitudes, nullability, defaults, índices, constraints, FKs, secuencias, propietarios de ir.model e ir.model.fields. Incluir res_country_state_cp. El port declara índices nuevos; incluso un update ORM puede crear DDL automáticamente, por eso no se ejecuta todavía.
4. **Un único dueño técnico.** Preferir actualizar direccion_mx manteniendo nombres de modelos, tablas e IDs. Comparar cada XML ID legado con los nuevos IDs: mantener o mapear explícitamente sin dejar que la limpieza de datos obsoletos borre registros. Revisar noupdate y propiedad de los registros importados. Si GMP llegó a instalarse, preparar un plan específico de metadatos; no asumir renombrado automático.
5. **Resolver CP y campos de contacto antes del update.** El modelo CP original existe y el port lo omite: no permitir que la limpieza del ORM lo retire sin decidir conservación. Su tabla y registros deben mantenerse. Preservar ciudad_id, municipio_id y colonia_id con los mismos IDs; definir city y l10n_mx_edi_colony según evidencia de almacenamiento real y consumidores.
6. **Ensayo futuro aislado.** Sólo después de revisar este plan, generar scripts versionados contra un esquema conocido y ejecutarlos en una copia desechable migrada, con logs completos. No se incluye ahora ningún script DDL ni hook de importación.
7. **Comparación posterior y reversión.** Comparar conjuntos de IDs y hashes de filas, no sólo conteos. Verificar cada FK desde res_partner y CP, inexistencia de huérfanos y duplicados nuevos, y secuencias por encima de max(id). Ante cualquier diferencia inesperada, rechazar el ensayo y restaurar otra copia del respaldo; no reparar borrando/recreando tablas ni reimportando CSV.

## Campo fiscal y city

Mantener el campo l10n_mx_edi_colony cuando exista o tenga consumidores, aunque CFDI esté fuera del alcance. Un related no almacenado no garantiza conservar el texto histórico ni la columna original; su cálculo puede ocultar diferencias. Comparar valores guardados y datos relacionados en copia antes de decidir store/related. Si l10n_mx_edi sigue instalado, revisar su definición Enterprise y posibles redefiniciones; no instalarlo sólo para resolver catálogos.

El cambio de city related a campo ordinario modifica el comportamiento en create/write/import y al renombrar ciudades. Definir si debe seguir al catálogo o admitir texto libre antes de modificarlo. No sobrescribir direcciones internacionales ni referencias existentes por inferencias automáticas.

## Riesgos y pruebas obligatorias

| Riesgo | Comprobación requerida |
|---|---|
| Pérdida por limpieza de modelos/XML IDs | CP y catálogo con mismos IDs/filas/metadatos; revisar logs de unlink/DDL |
| Duplicación | Un solo módulo propietario; mismas claves y huellas; cero importaciones CSV |
| Relaciones rotas | Comparación completa de contacto→ciudad/municipio/colonia y CP→catálogos |
| Permisos más amplios | Probar internos lectura, administradores según política; ACL aditivas y reglas antiguas |
| Direcciones inconsistentes | Ciudad/municipio/colonia por nombre y CP con ceros; cambios de país/estado; borrado de selección; APIs/imports, hijos y archivados |
| Texto fiscal/city alterado | Comparación de valores originales, definición store/related y consumidores de vistas/reportes |
| Vistas incompatibles | Validar formulario combinado, dominios, contactos hijos y compañías en Odoo 18 Enterprise |

Conteos históricos reportados: 645 ciudades, 3,060 municipios, 138,035 colonias; contactos con colonia 1,236, municipio 1,270, ciudad 1,234. **No medidos en esta sesión; no son criterios suficientes por sí solos.**

## Cambio implementado ahora

Únicamente el dominio de búsqueda de colonias en código LGPL-3 del repositorio. `_search_display_name` permite CP/nombre numérico y operadores negativos correctos; delega nombres normales al core. No cambia la base, esquema, IDs, vistas ni campos. Siete pruebas preparadas; resultados y límites en TEST_REPORT.md.

Fuentes exactas y commits: [SOURCE_REVIEW.md](SOURCE_REVIEW.md). Recursos indispensables: esquema/metadatos de copia 14, snapshot de datos y runtime Enterprise 18 desechable. No se necesita reimportar ni entregar los CSV para resolver estas brechas.
