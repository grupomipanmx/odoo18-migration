# Revisión técnica de direccion_mx y direccion_mx_gmp

Fecha: 2026-10-30  
Objetivo: preservar catálogos mexicanos y relaciones de contactos al pasar de Odoo 14 a Odoo 18.

## Fuentes examinadas
- ZIP aportado: carpeta `direccion_mx_gmp`.
- Repositorio original público: `jeffrepo/direccion_mx`, rama `master`.
- No se consultó ni modificó la base de datos productiva.

## Diferencias que impiden aprobar el módulo actual

1. **Nombre técnico distinto.** El módulo original se llama `direccion_mx`; el port inicial se llama `direccion_mx_gmp`. Los nombres de modelo coincidentes no hacen que Odoo transfiera automáticamente los metadatos del módulo original. No instalar ambos módulos con los mismos modelos activos.
2. **Vistas ausentes.** El manifiesto GMP declara `data: []`; no carga formularios, listas, menús ni vistas de contacto. Por tanto, aunque los modelos se registraran, no hay interfaz funcional incluida en este esqueleto.
3. **Seguridad ausente.** No se carga ningún `ir.model.access.csv`. Los modelos nuevos requieren permisos explícitos y mínimos.
4. **Campo `city` cambió de naturaleza.** El original define `city` como campo relacionado con `ciudad_id.name`; el port inicial lo trata como campo estándar y lo asigna por onchange. Esto puede cambiar almacenamiento, escritura y consistencia de datos.
5. **Campo SAT de colonia ausente.** El original expone `l10n_mx_edi_colony` como related a `colonia_id.name`; el port inicial no declara ese campo. Revisar integraciones y vistas que lo consuman antes de decidir si se conserva.
6. **Métodos heredados de dirección cambiaron.** El original modifica `_fields_view_get_address` para sustituir los campos de ciudad; el port no incluye una adaptación equivalente. La API del método también debe validarse en Odoo 18, no copiarse sin comprobar.
7. **Código postal/modelo CP.** El modelo `res.country.state.cp` debe compararse campo por campo con el esquema existente; la clase nueva añade `_rec_name`, índices y relaciones que no se deben aplicar a ciegas sobre una tabla poblada.
8. **Onchanges no son equivalentes.** El original tiene lógica de municipio/ciudad y respuestas onchange antiguas; el port asigna campos directamente. Hay que definir reglas funcionales correctas y evitar sobrescribir país/estado/ciudad de forma inesperada.
9. **Dependencias del manifiesto.** El original depende de `base_address_city` y `l10n_mx_edi`; el port sólo depende de `base` y `contacts`. CFDI queda fuera del alcance funcional actual, pero hay que detectar referencias residuales al campo de colonia SAT y no eliminar columnas/campos que aún tengan datos o dependencias.
10. **Carga de datos peligrosa.** El wizard original `post_install` importa CSV, realiza commits manuales y usa APIs obsoletas. No debe ejecutarse en el proceso de migración. El wizard de carga de direcciones también usa APIs antiguas. No reimportar CSV ni recrear IDs.

## Datos existentes reportados previamente en staging Odoo 14

- Ciudades: 645
- Municipios: 3,060
- Colonias: 138,035
- Contactos con `colonia_id`: 1,236
- Contactos con `municipio_id`: 1,270
- Contactos con `ciudad_id`: 1,234

Estos conteos son referencias de una revisión previa del staging, no una verificación ejecutada en esta sesión. La exportación previa de contactos contenía sólo `id` y cuatro campos de dirección, no era un respaldo integral de contactos.

## Diseño seguro recomendado

- Mantener un único propietario técnico de los modelos; no instalar `direccion_mx_gmp` en paralelo al módulo original.
- Antes de cambiar el nombre técnico, definir un plan de transición de módulo (renombrado/migración de metadatos) probado en una copia restaurable. La opción de menor riesgo es conservar el nombre técnico `direccion_mx` para la versión portada, si la arquitectura del repositorio y Odoo.sh lo permiten.
- Mantener los nombres de modelos y tablas existentes: `res_country_state_ciudad`, `res_country_state_municipio`, `res_country_state_municipio_colonia`; comprobar también la tabla del modelo CP.
- Comparar tipos, nullability, defaults, índices, secuencias, constraints, claves foráneas y conteos antes/después.
- Preservar IDs de ciudad/municipio/colonia y todas las referencias desde `res_partner`.
- Resolver explícitamente el diseño de `city`, `l10n_mx_edi_colony`, `zip`, `state_id` y `country_id`.
- Agregar vistas y permisos mínimos sólo después de validar el esquema y las APIs Odoo 18.
- Prohibido ejecutar wizard de importación, truncar tablas, recrear registros o aplicar SQL manual sobre producción.

## Validaciones pendientes para cerrar

1. Obtener del staging: estado instalado de `direccion_mx` y `direccion_mx_gmp`, módulos dependientes, campos/vistas que referencian `ciudad_id`, `municipio_id`, `colonia_id`, `city` y `l10n_mx_edi_colony`.
2. Comparar el esquema real con las definiciones originales y portadas, incluidas las claves foráneas.
3. Diseñar transición de metadatos del módulo con un script de migración Odoo 18 revisado y probado en copia.
4. Ejecutar pruebas de alta/edición de contactos, proveedores y clientes; seleccionar colonia por nombre y CP; verificar que ciudad/municipio/estado/país y CP quedan consistentes.
5. Comparar conteos, IDs y relaciones después de actualización.

## Estado

**NO APTO PARA INSTALACIÓN NI PARA PRUEBA UPGRADE.** El esqueleto GMP es un punto de partida, no un port completo. No ejecutar su instalación en la base de staging actual hasta resolver el conflicto potencial de modelos/metadatos y preparar migración de esquema.
