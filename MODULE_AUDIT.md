> Actualización de implementación: ahora hay dos addons. direccion_mx 18.0.2.1.0 recupera CP y define textos almacenados; pos_require_product_quantity 18.0.1.0.0 aporta el port de cantidades. Hay 8 ACL de direcciones y 3 XML en total. La cobertura inicial de 15 archivos que sigue es histórica; consultar TEST_REPORT.md para conteos actuales.

# Auditoría de módulos — Odoo 14 → 18

Fecha: 2026-10-30. Evidencia actual y hashes: [SOURCE_REVIEW.md](SOURCE_REVIEW.md). Los antecedentes del ZIP no sustituyen la lectura actual ni prueban el estado instalado en staging.

## Cobertura del repositorio de migración

Se revisaron sus 15 archivos originales: 7 Markdown y los 8 archivos del módulo. No contiene JavaScript, assets, scripts de migración, gitlinks, `.gitmodules`, configuración de servidor ni módulos Enterprise. Los tests y herramienta de esta entrega se revisaron después de agregarlos.

| Archivo/grupo | Hallazgo y decisión |
|---|---|
| README.md, MIGRATION_STATUS.md, MODULE_AUDIT.md | Mezclaban estado histórico y actual; actualizados con evidencia y bloqueos |
| POS_FUNCTIONAL_REVIEW.md, DIRECCION_MX_TECHNICAL_GAPS.md | Actualizados con fuentes históricas accesibles y brechas vigentes |
| ZIP_REVIEW_2026-10-30.md, STATIC_CHECKS_2026-10-30.md | Conservados con aviso de antecedentes; ZIP no disponible localmente |
| direccion_mx/__manifest__.py | LGPL-3 declarada, 18.0.2.0.0, depende de base/contacts; carga ACL y dos vistas; sin CSV ni hooks. installable=True no prueba instalación |
| direccion_mx/__init__.py, models/__init__.py | Cadena de imports presente; modelos se importan; sin efectos externos fuera del registro ORM |
| models/address_catalog.py | Cuatro modelos con tablas explícitas; CP recuperado con los cuatro campos originales, sin índices/requisitos nuevos. Índices anteriores requieren comparar esquema. `_name_search` no es extensión efectiva en 18: corregido a `_search_display_name` |
| models/res_partner.py | Relaciones existentes conservadas; city/colonia fiscal ahora almacenados, con valores explícitos prioritarios. create/write completan selecciones explícitas; edición ajena a direcciones no reescribe vínculos. Cambio de país/estado y limpieza de CP deben especificarse |
| views/address_catalog_views.xml | list/form y view_mode list,form usan sintaxis 18; menús para group_system. Edición/eliminación permitidas a administradores por ACL; revisar necesidad antes de uso |
| views/res_partner_views.xml | Hereda base.view_partner_form, inserta tras zip. Ref existe en core 18; xpath amplio en formulario con direcciones anidadas: probar vista combinada y readonly de contactos hijos. Ciudad sin dominio por estado; municipio sólo filtrado por estado |
| security/ir.model.access.csv | Ocho ACL: internos lectura; sistema CRUD, incluido CP. No filas públicas. ACL son aditivas: reglas/ACL heredadas podrían ampliar permisos, no verificables sin BD |

El seguimiento añade CP, redefine almacenamiento de textos y prepara migrations/18.0.2.1.0/pre-migrate.py y post-migrate.py; no se ejecutaron contra Odoo. No hay hooks de importación. El pre bloquea esquema inesperado/huérfanos; post rellena sólo NULL. Falta demostrar registry y conservación en PostgreSQL real.

## Históricos y submódulos

Se accedió autenticadamente a `jeffrepo/grupomipan`, rama `odoo18-migration`, y su `.gitmodules`. Los 12 gitlinks se registran con commit en SOURCE_REVIEW. No se usó `submodule update --recursive`, para evitar copiar código propietario. Se consultaron por separado repositorios de las dependencias permitidas.

| Módulo | Evidencia/licencia | Resultado para 18 |
|---|---|---|
| direccion_mx | Legado e3aed4a; manifiesto sin licencia explícita; sólo consultado | base_address_city/l10n_mx_edi/contacts; name_get y manipulación antigua de vistas. No copiar/importar catálogos |
| direccion_mx_gmp | Fuentes históricos consultados; LGPL-3 declarada | data vacío, sin ACL/vistas, name_get legado, CP presente; no instalar junto al original |
| disable_trash_pos_order | JS y XML consultados; sin licencia expresa en manifiesto | Registries.Component.extend/TicketScreen y assets legacy; puede fallar si order.employee no existe. Sólo oculta botón; no control backend |
| pos_hide_today_orders | LGPL-3, reglas y override consultados | Reemplaza globalmente ir.rule._eval_context; no reproducir. Fecha basada en user.login_date.now/timezone, sin zona por defecto. Regla también aplica a unlink |
| pos_print_group | AGPL-3, fuentes consultados | PosModel/get_cashier, ReceiptScreen y point_of_sale.assets legacy; depende de empleado/cajero y grupos cargados. Necesita adaptación y prueba de impresión automática/reimpresión |
| sh_pos_order_list | OPL-1 según reporte histórico | Pedir paquete Odoo 18. No copiar, modificar ni redistribuir |
| sh_pos_order_sync | OPL-1, depende de sh_pos_order_list según reporte | Pedir ambos paquetes 18 y migración coordinada; concurrencia/reconexión pendientes |
| aspl_pos_order_sync_ee | Gitlink comercial 2800fe5; restricción según histórico | Pedir versión Enterprise 18; confirmar si se usa junto a Softhealer. No duplicar motores de sincronización |
| pos_require_product_quantity | AGPL-3, fuentes del gitlink consultados | `_onClickPay` legacy llama super antes de validar; flag require_product_quantity no se consulta en JS. Implementado port 18: PosStore.pay/PaymentScreen.validateOrder antes de super, guardia servidor y restricción al finalizar; 4 tests ORM pendientes y 11 JS locales aprobados |
| pos_receipt_client | LGPL-3, QWeb del gitlink consultado | Añade cliente Y nota por línea. props.order.orderlines.find(...).note sin guardia; qweb/estructura recibo legacy. Depende de pos_restaurant |
| pos_loyalty_fields | Sin licencia expresa en manifiesto; vistas consultadas | Grupos sobre loyalty_points y ClientDetailsEdit legacy. No asumir equivalencia con lealtad 18 ni reinstalar |
| stock_account_purchase | Cabeceras AGPL-3; modelos y vista consultados | Omite asientos por proveedor; retorna False donde 18 consume lista; falta dependencia explícita purchase_stock. Ver STOCK_ACCOUNT_REVIEW |
| mass_editing | AGPL-3; manifiesto y revisión estática dirigida de fuentes | fields_view_get, attrs/tree, creación dinámica, ir.translation y sudo requieren port. Migraciones 14 contienen ALTER/UPDATE/DELETE; NO ejecutar. Tests remotos existentes, no ejecutados |
| web_m2x_options | AGPL-3; manifiesto y revisión estática dirigida de fuentes | web.relational_fields, Dialog/data/rpc, include/extend legacy y qweb; sustituir por paquete compatible si necesario. Tests remotos no ejecutados |
| factura_global, factura_global_complemento, validar_facturas, l10n_mx_edi_cancel | Gitlinks inventariados | Fuera de alcance funcional; falta verificar dependencias instaladas y metadatos en BD. No reinstalar/desinstalar automáticamente |

## APIs y dependencias

- Odoo 18 `name_search` busca display_name y combina args; la extensión local usa `_search_display_name`. Para CP numérico combina nombre/CP por OR; operadores negativos requieren AND. No usa sudo ni SQL. El dominio del llamador y las reglas los aplica el ORM.
- En POS se observaron referencias concretas a Registries, PosModel, pantallas importadas por nombres antiguos y herencia de point_of_sale.assets. Odoo 18 declara `point_of_sale._assets_pos`; es necesario adaptar imports/componentes/servicios/payloads. `odoo.define` por sí solo no demuestra toda incompatibilidad.
- `name_get`, `fields_view_get`, manifiestos `qweb`/`init_xml`, `attrs`, `tree` y dominios devueltos por onchange requieren revisión en cada fuente legacy; no se aplicó una sustitución textual indiscriminada.
- base/contacts existen en core; contacts depende de base/mail, por lo que tracking tiene dependencia transitiva. Se verificaron los XML IDs de formulario partner y menú contacts en fuente oficial. La resolución en el registry real y dependencias Enterprise sigue pendiente.
- No se ha comprobado que las desinstalaciones reportadas eliminen referencias en vistas Studio, acciones, reglas o datos. Tampoco se han reproducido los errores TestCrawler/AccessError.

## Criterio de cierre

Sólo puede recomendarse Upgrade tras comparar datos/metadatos y completar instalación, actualización y pruebas funcionales Enterprise. La auditoría de código disponible está documentada; la auditoría de la BD y los módulos comerciales permanece pendiente. **NO APTO.**
