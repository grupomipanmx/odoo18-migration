# Reporte de pruebas reales — seguimiento 2026-10-30

Rama: codex/odoo18-compatibility. Código de direcciones publicado en 40173bb8ee6b90d524ac20df6ee3333f4ad93f08; control POS en 75d9a69275ab26ade590231148f9d172ff1832b8. Esta ejecución incluye la protección adicional del empaquetador contra salida dentro del addon y la documentación final. No se conectó a una BD Odoo, no se desplegó ni se modificó producción.

## Resultado comprobado

| Área | Resultado | Alcance real |
|---|---|---|
| Python local | 12 tests PASS | 6 comparador, 3 paquete puente, 3 backfill sintético |
| JavaScript local | 11 tests PASS | 5 lógica de cantidades y 6 patch bodies con dobles explícitos; no OWL/browser/servicios reales |
| Backfill | PASS en SQLite en memoria | Script post real ejecutado sobre fixtures sintéticos; conserva IDs/vínculos/proveedor, texto no NULL y vacío; idempotencia. No PostgreSQL ni loader de migración Odoo |
| Python/XML/manifiestos/ACL/assets | PASS estático | 23 Python, 3 XML, 2 manifiestos, 8 ACL direcciones y 2 assets locales. Sin registry Enterprise |
| Tests ORM | 24 preparados: 20 direcciones y 4 POS | No ejecutados: importación falla por ausencia de odoo. El contador del cargador unittest no representa casos funcionales aprobados |
| Instalación, Upgrade, sincronización y pagos | NOT RUN | Sin runtime 18 Enterprise/PostgreSQL/paquetes comerciales autorizados configurados |
| Preservación real de catálogos/contactos | NOT RUN | Snapshot/exporter y comparación implementados; no se capturó baseline de ninguna base real |

## Errores observados y corrección

La primera ejecución de los tres tests nuevos del backfill falló en SQLite con `OperationalError: near "p": syntax error`, porque el alias de UPDATE no llevaba AS. Se explicitó `UPDATE res_partner AS p`, compatible con la sintaxis usada en PostgreSQL y aceptado en la prueba SQLite. Después pasaron los tres casos. Ese fallo y su corrección no se presentan como una prueba de instalación Odoo.

La ejecución de tests ORM vuelve a fallar al importar por `ModuleNotFoundError: No module named 'odoo'`. No se ocultó ni se sustituyó por resultados inventados. Python local 3.15.0, sin odoo/psycopg2/lxml ni ejecutables docker/psql/postgres/pg_ctl detectables. No se intentó instalar sobre staging 14 ni sobre producción para compensar esa falta.

Las consultas directas a las fichas comerciales 18 recibieron 429/no disponible; una búsqueda oficial recuperó la ficha de sh_pos_order_list 18 y referencias al producto de sincronización. Eso no proporciona el paquete, licencia de la instalación ni una prueba funcional.

## Cobertura pendiente Odoo

CP con tabla/tamaño/opcionalidad originales; integridad de IDs y relaciones tras edición; city/colonia fiscal almacenados; alta desde catálogos por API; texto explícito y direcciones internacionales; proveedores/archivados; limpieza de selectores sin perder texto; renombrados; lotes; rechazo de incoherencias; hijos y ACL. Se mantienen siete tests originales de búsqueda.

POS: borrador con cero puede guardarse pero no finalizar, flag desactivado, fracciones/devoluciones y rechazo de state paid vía RPC. Falta instalación, actualización y prueba del core con sus excepciones/stock, bundle real, navegador, proveedor de sincronización, concurrencia, reconexión y contabilización. El usuario exige sincronización desde el primer día.

## Comandos y salida capturada

## `python -m unittest discover -s tests -p test_*.py -v`

Salida: **0**.

```text
test_backfill_materializes_names_without_changing_links_or_supplier (test_address_backfill.TestAddressBackfill.test_backfill_materializes_names_without_changing_links_or_supplier) ... ok
test_existing_text_and_explicit_empty_values_survive (test_address_backfill.TestAddressBackfill.test_existing_text_and_explicit_empty_values_survive) ... ok
test_second_execution_is_idempotent (test_address_backfill.TestAddressBackfill.test_second_execution_is_idempotent) ... ok
test_bridge_preserves_all_field_and_table_declarations (test_address_bridge.TestAddressBridge.test_bridge_preserves_all_field_and_table_declarations) ... ok
test_existing_output_cannot_be_overwritten (test_address_bridge.TestAddressBridge.test_existing_output_cannot_be_overwritten) ... ok
test_output_inside_addon_source_is_rejected (test_address_bridge.TestAddressBridge.test_output_inside_addon_source_is_rejected) ... ok
test_changed_relation_or_text_digest_fails (test_address_integrity.TestAddressIntegrity.test_changed_relation_or_text_digest_fails) ... ok
test_identical_snapshot (test_address_integrity.TestAddressIntegrity.test_identical_snapshot) ... ok
test_incomplete_snapshot_fails (test_address_integrity.TestAddressIntegrity.test_incomplete_snapshot_fails) ... ok
test_missing_cp_is_not_accepted (test_address_integrity.TestAddressIntegrity.test_missing_cp_is_not_accepted) ... ok
test_recreated_ids_fail_even_if_count_is_unchanged (test_address_integrity.TestAddressIntegrity.test_recreated_ids_fail_even_if_count_is_unchanged) ... ok
test_table_change_fails (test_address_integrity.TestAddressIntegrity.test_table_change_fails) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.069s

OK
```

## `node --test tests/test_pos_quantity.mjs tests/test_pos_payment_guard.mjs`

Salida: **0**.

```text
✔ zero quantity never calls the standard payment flow (3.9456ms)
✔ valid sale calls the base payment flow after capture (0.9717ms)
✔ pending number-buffer value is checked before payment (0.4437ms)
✔ direct validation is blocked before standard removal/payment code (0.3941ms)
✔ refund validation delegates arguments to standard behavior (0.4715ms)
✔ disabled flag allows both normal entry points (0.5065ms)
✔ blocks zero quantities (2.7082ms)
✔ configuration disabled keeps the standard flow (0.2788ms)
✔ allows fractional quantities and refunds (0.2193ms)
✔ rejects non-finite and malformed quantities (0.3469ms)
✔ handles absent and empty orders (0.2489ms)
ℹ tests 11
ℹ suites 0
ℹ pass 11
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 565.6187
```

## `python tools/check_repository.py`

Salida: **0**.

```text
{
  "python": "3.15.0",
  "python_files": 23,
  "xml_files": 3,
  "modules": {
    "direccion_mx": {
      "license_declared": "LGPL-3",
      "depends": [
        "base",
        "contacts"
      ],
      "data_files": 3,
      "acl_rows": 8,
      "external_dependencies_installed": "NOT_VERIFIED"
    },
    "pos_require_product_quantity": {
      "license_declared": "AGPL-3",
      "depends": [
        "point_of_sale"
      ],
      "data_files": 1,
      "acl_rows": 0,
      "external_dependencies_installed": "NOT_VERIFIED"
    }
  },
  "odoo_tests_discovered_not_executed": [
    "direccion_mx/tests/test_address_preservation.py::test_legacy_tables_and_cp_definition",
    "direccion_mx/tests/test_address_preservation.py::test_cp_optional_relations_and_existing_id_survive_edit",
    "direccion_mx/tests/test_address_preservation.py::test_create_from_colony_completes_server_side",
    "direccion_mx/tests/test_address_preservation.py::test_create_from_city_and_municipality",
    "direccion_mx/tests/test_address_preservation.py::test_explicit_text_is_preserved_in_import_values",
    "direccion_mx/tests/test_address_preservation.py::test_free_text_without_mx_catalogs",
    "direccion_mx/tests/test_address_preservation.py::test_supplier_archived_contact_and_ids_survive_unrelated_write",
    "direccion_mx/tests/test_address_preservation.py::test_clearing_selectors_keeps_saved_address_text",
    "direccion_mx/tests/test_address_preservation.py::test_catalog_rename_preserves_partner_text_and_ids",
    "direccion_mx/tests/test_address_preservation.py::test_batch_create_and_write",
    "direccion_mx/tests/test_address_preservation.py::test_conflicting_catalog_links_are_rejected_without_replacing_ids",
    "direccion_mx/tests/test_address_preservation.py::test_parent_address_sync_includes_catalog_relations",
    "direccion_mx/tests/test_address_preservation.py::test_cp_read_permissions_do_not_allow_catalog_creation",
    "direccion_mx/tests/test_colonia_search.py::test_postal_code_keeps_leading_zero_and_matches_numeric_name",
    "direccion_mx/tests/test_colonia_search.py::test_normal_name_search",
    "direccion_mx/tests/test_colonia_search.py::test_negative_match_excludes_postal_code_and_name",
    "direccion_mx/tests/test_colonia_search.py::test_negative_equality_excludes_both_fields",
    "direccion_mx/tests/test_colonia_search.py::test_caller_domain_is_preserved",
    "direccion_mx/tests/test_colonia_search.py::test_empty_term_and_limit",
    "direccion_mx/tests/test_colonia_search.py::test_internal_user_read_only_and_record_rule",
    "pos_require_product_quantity/tests/test_quantity_guard.py::test_draft_can_sync_zero_quantity_but_cannot_finalize",
    "pos_require_product_quantity/tests/test_quantity_guard.py::test_disabled_configuration_preserves_standard_behavior",
    "pos_require_product_quantity/tests/test_quantity_guard.py::test_fractional_sale_and_negative_refund_are_allowed",
    "pos_require_product_quantity/tests/test_quantity_guard.py::test_rpc_cannot_set_zero_quantity_order_paid"
  ],
  "runtime": {
    "odoo": false,
    "psycopg2": false,
    "lxml": false
  },
  "executables": {
    "docker": null,
    "psql": null,
    "postgres": null,
    "pg_ctl": null
  },
  "errors": [],
  "static_result": "PASS",
  "installation_upgrade_result": "NOT_RUN"
}
```

## `python -m compileall -q direccion_mx pos_require_product_quantity tools tests`

Salida: **0**.

```text

```

## `node --check pos_require_product_quantity/static/src/payment_guard.js`

Salida: **0**.

```text

```

## `node --check pos_require_product_quantity/static/src/quantity_validation.js`

Salida: **0**.

```text

```

## `git diff --check`

Salida: **0**.

```text
warning: in the working copy of 'direccion_mx/tests/__init__.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tools/check_repository.py', LF will be replaced by CRLF the next time Git touches it
```

## `python -m unittest direccion_mx.tests.test_address_preservation pos_require_product_quantity.tests.test_quantity_guard`

Salida: **1**.

```text
EE
======================================================================
ERROR: direccion_mx (unittest.loader._FailedTest.direccion_mx)
----------------------------------------------------------------------
ImportError: Failed to import test module: direccion_mx
Traceback (most recent call last):
  File "C:\Users\siste\AppData\Local\Python\pythoncore-3.15-64\Lib\unittest\loader.py", line 141, in loadTestsFromName
    module = __import__(module_name)
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\direccion_mx\__init__.py", line 1, in <module>
    from . import models
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\direccion_mx\models\__init__.py", line 1, in <module>
    from . import address_catalog
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\direccion_mx\models\address_catalog.py", line 3, in <module>
    from odoo import api, fields, models
ModuleNotFoundError: No module named 'odoo'


======================================================================
ERROR: pos_require_product_quantity (unittest.loader._FailedTest.pos_require_product_quantity)
----------------------------------------------------------------------
ImportError: Failed to import test module: pos_require_product_quantity
Traceback (most recent call last):
  File "C:\Users\siste\AppData\Local\Python\pythoncore-3.15-64\Lib\unittest\loader.py", line 141, in loadTestsFromName
    module = __import__(module_name)
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\pos_require_product_quantity\__init__.py", line 1, in <module>
    from . import models
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\pos_require_product_quantity\models\__init__.py", line 1, in <module>
    from . import pos_config
  File "C:\Users\siste\OneDrive\Documentos\ChatGPT\14_18 odoo\odoo18-migration\pos_require_product_quantity\models\pos_config.py", line 2, in <module>
    from odoo import api, fields, models
ModuleNotFoundError: No module named 'odoo'


----------------------------------------------------------------------
Ran 2 tests in 0.003s

FAILED (errors=2)
```

## Dictamen

**NO APTO para declarar una migración funcional a Odoo 18.** Hay implementación y 23 pruebas locales aprobadas (12 Python + 11 JS), pero no evidencia de instalación/actualización/ORM Enterprise ni sincronización obligatoria. El puente se empaquetó en tests, nunca se instaló. El pre-migrate PostgreSQL sólo fue compilado/revisado; el post se ejercitó en SQLite sintético. El detalle de la ruta de cierre está en POS_FIRST_UPGRADE.md y STAGING_RUNBOOK.md.
