# Reporte de pruebas reales — 2026-10-30

Repositorio: grupomipanmx/odoo18-migration. Rama: codex/odoo18-compatibility. Base auditada: 318677df86c611d16bf54c0c59869a5c1a901934. Entorno Windows local, Python 3.15.0. No se conectó a ninguna BD ni a Odoo.sh. No se ejecutaron importaciones de catálogos, instalación ni actualización.

| Comprobación | Resultado real | Límite |
|---|---|---|
| Compilación Python | PASS, 8 archivos incluyendo herramienta y tests | Sintaxis bajo Python 3.15, no runtime Odoo 18 |
| XML | PASS, 2 archivos bien formados | Sin validación de herencia/vistas por registry |
| Manifiesto y ACL | PASS local: 1 módulo, 3 archivos declarados existentes, 6 ACL con modelo local y grupo explícito | Grupos, reglas heredadas y dependencias instaladas requieren Odoo |
| Dependencias | base/contacts declaradas; corroboradas en fuente oficial; contacts→base/mail | No instaladas ni resueltas por registry Enterprise |
| Tests nuevos | 7 casos descubiertos estáticamente; ejecución bloqueada al importar | ModuleNotFoundError: odoo; no hay siete tests aprobados |
| Tests de submódulos | Se identificaron tests remotos mass_editing/web_m2x_options | No copiados al target ni ejecutados; requieren Odoo y su versión compatible |
| Instalación/actualización | NOT RUN | Sin runtime Odoo/Enterprise, PostgreSQL ni copia desechable configurada; plan de esquema pendiente |
| JS/assets/frontend y funcionales | NOT RUN | Target sin JS; originales revisados en lectura, sin navegador POS 18 |
| Integridad de BD | NOT RUN | Conteos/IDs/relaciones no medidos; números históricos no validados |

Los siete casos preparados cubren CP con cero inicial/nombre numérico, nombre normal, negación ilike, desigualdad, dominio adicional, consulta vacía/límite y lectura con regla/denegación de creación para usuario interno. TransactionCase está diseñado para aislar fixtures, pero no se ejecutó aquí. El mensaje unittest «Ran 1 test» corresponde al error del cargador, no a una prueba funcional ejecutada.

## Auditoría de entorno y fuentes

Se ejecutaron git status/remote/log/ls-files, rg --files y lecturas de todos los archivos del target. `git ls-remote` verificó main original 318677d y ausencia remota de la rama de trabajo antes de crearla. El checkout inicial ERP_JM_LITE tenía cambios ajenos y quedó intacto; se creó una copia separada del repositorio solicitado.

`python --version` y `py --list` identificaron únicamente Python 3.15.0. `Get-Command` y la sonda importlib/shutil de la herramienta no detectaron odoo, psycopg2, lxml ni docker/psql/postgres/pg_ctl en el entorno local. Esto no prueba ausencia de un servidor remoto: su acceso no estaba configurado.

Se consultó por GitHub autenticado el histórico privado, .gitmodules, su árbol y submódulos permitidos; hashes en SOURCE_REVIEW.md. La consulta anónima del histórico devolvió 404; autenticada funcionó. Se verificaron en fuente Odoo 18 los métodos name_search/_search_display_name, el retorno de _account_entry_move y su consumidor, purchase_id de purchase_stock, bundle POS y XML IDs base.view_partner_form/contacts.menu_contacts. No equivale a instalar addons. Las consultas web a documentación ORM/JS fallaron y se usaron fuentes oficiales de código.

## Salida capturada de los comandos reproducibles

## `python tools/check_repository.py`

Código de salida: **0**.

```text
{
  "python": "3.15.0",
  "python_files": 8,
  "xml_files": 2,
  "modules": {
    "direccion_mx": {
      "license_declared": "LGPL-3",
      "depends": [
        "base",
        "contacts"
      ],
      "data_files": 3,
      "acl_rows": 6,
      "external_dependencies_installed": "NOT_VERIFIED"
    }
  },
  "odoo_tests_discovered_not_executed": [
    "direccion_mx/tests/test_colonia_search.py::test_postal_code_keeps_leading_zero_and_matches_numeric_name",
    "direccion_mx/tests/test_colonia_search.py::test_normal_name_search",
    "direccion_mx/tests/test_colonia_search.py::test_negative_match_excludes_postal_code_and_name",
    "direccion_mx/tests/test_colonia_search.py::test_negative_equality_excludes_both_fields",
    "direccion_mx/tests/test_colonia_search.py::test_caller_domain_is_preserved",
    "direccion_mx/tests/test_colonia_search.py::test_empty_term_and_limit",
    "direccion_mx/tests/test_colonia_search.py::test_internal_user_read_only_and_record_rule"
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

## `python -m compileall -q direccion_mx tools`

Código de salida: **0**.

```text

```

## `git diff --check`

Código de salida: **0**.

```text

```

## `python -m unittest direccion_mx.tests.test_colonia_search`

Código de salida: **1**.

```text
E
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


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)
```

## Dictamen

**NO APTO para prueba de Upgrade.** La corrección tiene comprobación sintáctica y siete casos preparados, pero falta evidencia de ORM, instalación, actualización, conservación de datos y aceptación funcional Enterprise. Requisitos y secuencia futura en STAGING_RUNBOOK.md. No se afirma haber repetido las pruebas del ZIP histórico.
