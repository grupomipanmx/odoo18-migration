# Fuentes consultadas — 2026-10-30

La auditoría local parte de `318677df86c611d16bf54c0c59869a5c1a901934`. Se consultaron fuentes remotas en modo lectura; no se copiaron módulos comerciales al repositorio de migración. El ZIP no está adjunto al entorno actual; sus reportes anteriores se conservan como históricos.

## Proyecto histórico

Cuenta conectada: Mi Pan. Repositorio privado `jeffrepo/grupomipan`, rama `odoo18-migration`; árbol Git `7b521bf90a844e73d06f7bca6d224e76dfa37872`. `.gitmodules` blob `ec6c41254582615188637f9378d3c5952fe016cc`. El acceso anónimo devolvió 404; la lectura autenticada sí funcionó. No se escribió en ese repositorio.

| Submódulo | Repositorio según .gitmodules | Commit fijado |
|---|---|---|
| aspl_pos_order_sync_ee | jeffrepo/aspl_pos_order_sync_ee | `2800fe5eec912c407ed036727729091641588cdf` |
| direccion_mx | jeffrepo/direccion_mx | `e3aed4a499c3617644d47afa87b716dc48f0277d` |
| factura_global | jeffrepo/factura_global | `fea0681c4b7109ff7c46ee6cd73e5681f0bdd52c` |
| factura_global_complemento | jeffrepo/factura_global_complemento | `94a6c41752137861f8ec53a016ea369c0a1603a1` |
| l10n_mx_edi_cancel | jeffrepo/l10n_mx_edi_cancel | `c4af36ec749b0a9d991dff53d0712ecdf249f5cc` |
| mass_editing | jeffrepo/mass_editing | `c0af2dffac1ea374babaa90ff4da417e8f90aefb` |
| pos_loyalty_fields | jeffrepo/pos_loyalty_fields | `32a9bcb74f383083acd0c239c7d3ea4c00bdf3b1` |
| pos_receipt_client | jeffrepo/pos_receipt_client | `0a9bbf80b4c4aade0f43be6b94b7ba0b5666a588` |
| pos_require_product_quantity | jeffrepo/pos_require_product_quantity | `8a0c25b07fc54e1d605242cd2a8d7318982da09b` |
| stock_account_purchase | jeffrepo/stock_account_purchase | `a3594d2ac577c0c491933ca743de46fcf20fb160` |
| validar_facturas | jeffrepo/validar_facturas | `8835cb1f9e7858782381e5ded89fbc45ce04113b` |
| web_m2x_options | jeffrepo/web_m2x_options | `01c988201734a481519bf27b99417a79f496a11c` |

## Archivos históricos consultados

Se registran referencias y hashes, sin redistribuir los fuentes. Softhealer/ASPL quedan limitados al inventario y a los hallazgos históricos; no se descargaron sus fuentes en esta revisión.

| Repositorio / archivo | Blob |
|---|---|
| jeffrepo/grupomipan/direccion_mx_gmp/__manifest__.py | `4d9fe42764982cbc0d3f0acd8c8a971f955a3adc` |
| jeffrepo/grupomipan/disable_trash_pos_order/__manifest__.py | `f4f48131c680695c659fb807b9856eb7025da770` |
| jeffrepo/grupomipan/pos_hide_today_orders/__manifest__.py | `4f20ea61e75fa0f49622ab3282d3e2730346f870` |
| jeffrepo/grupomipan/pos_print_group/__manifest__.py | `c046ef4d47364007e8330ac4032ac84a351c6437` |
| jeffrepo/pos_loyalty_fields/__manifest__.py | `78d6e0b1143fc1018c9fec16f80e61b7169b95ee` |
| jeffrepo/pos_receipt_client/__manifest__.py | `cc11dfd6a9fd48c9361c59d6e03abea5bb262f9c` |
| jeffrepo/pos_require_product_quantity/__manifest__.py | `8d39c733c2053517eb13223c162a37e2a5534653` |
| jeffrepo/mass_editing/__manifest__.py | `6c61e6cf6fb57a65ce1bd2cc677b363e4e6939bf` |
| jeffrepo/web_m2x_options/__manifest__.py | `6863e2e9cefb34ff68872c9a9ef4c301099e05ec` |
| jeffrepo/grupomipan/direccion_mx_gmp/__init__.py | `0650744f6bc69b9f0b865e8c7174c813a5f5995e` |
| jeffrepo/grupomipan/direccion_mx_gmp/models/__init__.py | `26ad407896f13b49c3f297fd3f562c42d6290fc0` |
| jeffrepo/grupomipan/direccion_mx_gmp/models/address_catalog.py | `c6c789017b3a616f1a7011686db8d614214fc6d4` |
| jeffrepo/grupomipan/direccion_mx_gmp/models/res_partner.py | `9f9d83f97b0f631f6976ad12b4f6bbafaf4ca248` |
| jeffrepo/grupomipan/disable_trash_pos_order/__init__.py | `d1d81f4b73e6c243e626764f5c3cc7791c7d4bde` |
| jeffrepo/grupomipan/disable_trash_pos_order/static/src/js/Screens/OrderScreen/TicketScreen.js | `dd86e2f856f5341701c71a0fd0d1fddae69a5a78` |
| jeffrepo/grupomipan/disable_trash_pos_order/views/pos_assets.xml | `045aa5f3b12ea6a22f2dc9e4b101c1098745ca7c` |
| jeffrepo/grupomipan/pos_hide_today_orders/__init__.py | `a0fdc10fe11b9eb562881952079e34c2982f8604` |
| jeffrepo/grupomipan/pos_hide_today_orders/models/__init__.py | `3605b081ff3c801274cd5e3f6d989c9c5644d7b5` |
| jeffrepo/grupomipan/pos_hide_today_orders/models/ir_rule.py | `5154f7457c084c15beb9eb671e6dff09cbbd15bc` |
| jeffrepo/grupomipan/pos_hide_today_orders/security/groups.xml | `93dec016ee56c7ab2e4db7a7b46a1a4f5890766b` |
| jeffrepo/grupomipan/pos_hide_today_orders/security/rules.xml | `8b8aea69d654323aefa0691229fefd63b2c3073f` |
| jeffrepo/grupomipan/pos_print_group/__init__.py | `0650744f6bc69b9f0b865e8c7174c813a5f5995e` |
| jeffrepo/grupomipan/pos_print_group/models/__init__.py | `db8634ade1f78b0e64ab570d301a8626c65b0703` |
| jeffrepo/grupomipan/pos_print_group/models/pos_config.py | `ba130d0889173d259dcfeab6002475cfd5f92c33` |
| jeffrepo/grupomipan/pos_print_group/security/res_groups.xml | `813daf1f505e5b0ab4e35fd77d2c7bd7d81e9b60` |
| jeffrepo/grupomipan/pos_print_group/static/src/js/ReceiptScreen.js | `e3367e207a5bf1b972cdbc1d3e1526fb4f438a0e` |
| jeffrepo/grupomipan/pos_print_group/static/src/js/models.js | `45eed047929f9635827fc50947957c7abe3365c3` |
| jeffrepo/grupomipan/pos_print_group/views/templates.xml | `e3037cc077289c0b758266ebfac2aa7a59c7d125` |
| jeffrepo/pos_require_product_quantity/models/pos_config.py | `05859a7778db0e9366797669ab2717e85913563e` |
| jeffrepo/pos_require_product_quantity/static/src/js/screens.js | `a38b8982048d16adaad97c31cab728babb2750dc` |
| jeffrepo/pos_require_product_quantity/views/assets.xml | `f27b6a861cc4d891884f9e3daf212998425c45a1` |
| jeffrepo/pos_require_product_quantity/views/pos_config.xml | `1b86ab214fd45ab04786798913d5fba841ddafcb` |
| jeffrepo/pos_receipt_client/static/src/xml/OrderReceipt.xml | `71bb2fe5636a060304481cf57e52ee8f9e850053` |
| jeffrepo/pos_loyalty_fields/security/groups.xml | `a87d53615ad9874a78ded82893bd43f1f059adfa` |
| jeffrepo/pos_loyalty_fields/static/src/xml/pos_loyalty_views.xml | `0524de89a01857d4d42b066b29a4ef21ec185ad8` |
| jeffrepo/pos_loyalty_fields/views/pos_loyalty_views.xml | `21d8a8c6ec0b5552895f1d4da79de650efd605ad` |
| jeffrepo/mass_editing/demo/mass_editing.xml | `c06c23a05b18c4fd6a11108784ab4eb52dc8ebf7` |
| jeffrepo/mass_editing/migrations/14.0.1.0.0/post-migrate.py | `b9186754c5143d4f270c808b1096364e68cd3106` |
| jeffrepo/mass_editing/migrations/14.0.1.0.0/pre-migrate.py | `2ddd83aef7177011293578deaf56c6cff58b3671` |
| jeffrepo/mass_editing/models/ir_actions_server.py | `9435cbb8e35d1f05e0d7f8508ddf391163ee5d7b` |
| jeffrepo/mass_editing/models/mass_editing_line.py | `6987e05835e19f02037b0fde4fc9357deca9a758` |
| jeffrepo/mass_editing/security/ir.model.access.csv | `4fa87284e85e16606acb3ae7d234b9e3a137d1fb` |
| jeffrepo/mass_editing/tests/test_mass_editing.py | `028fd7309e85fae9d9f7abd3d6e777a71c5e2e4d` |
| jeffrepo/mass_editing/views/ir_actions_server.xml | `69ff9cf4032ca1dcc57e344b8d76c86aca8d8521` |
| jeffrepo/mass_editing/wizard/mass_editing_wizard.py | `7dc01a5a8136c68ee1e4e510fd349c1eab7758c8` |
| jeffrepo/mass_editing/wizard/mass_editing_wizard.xml | `27b2fe42a1bbcbd63dfe40e44097c7b1608c69d3` |
| jeffrepo/web_m2x_options/models/ir_config_parameter.py | `8e7228f086e875ced654ae1d582729ffbcbbb6eb` |
| jeffrepo/web_m2x_options/static/src/js/form.js | `de54a9d83efd82db65b62b52fb69f6b9dde8bda9` |
| jeffrepo/web_m2x_options/static/src/xml/base.xml | `a4f5ae3c7dfd4048fff880cfc33345eb83702e5f` |
| jeffrepo/web_m2x_options/tests/test_ir_config_parameter.py | `1b78bae66bb7df3b18cc4ff25046abed721def47` |
| jeffrepo/web_m2x_options/views/view.xml | `d2be9152ec3c7374deb9a989a164b39aa996e43a` |

## Fuentes públicas de comparación

- [ORM Odoo 18](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/odoo/models.py): `_search_display_name`, `name_search`; SHA256 consultado `d978173f4a1a3f0702b081451ecc2936a1cc8d40fddcbe1043a277c0a566c86a`.
- [Valoración Odoo 18](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/addons/stock_account/models/stock_move.py); SHA256 `1ac68e6eef8c2cb13ab723cac7cabeda4f4d44999d123f95c278b2f58b449043`.
- [Consumidor de asientos de valoración](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/addons/stock_account/models/stock_valuation_layer.py).
- [purchase_stock](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/addons/purchase_stock/models/stock.py); SHA256 `aa4b0cdf65e3a5a1e272d4a3b041665f7066843d3ee411f6c3ecf3068dbb0c90`.
- [Assets POS](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/addons/point_of_sale/__manifest__.py).
- [Formulario partner](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/odoo/addons/base/views/res_partner_views.xml) y [menú contacts](https://github.com/odoo/odoo/blob/54c0991d2949bf4090231c8c167b4a1038769085/addons/contacts/views/contact_views.xml).
- [direccion_mx legado](https://github.com/jeffrepo/direccion_mx/tree/e3aed4a499c3617644d47afa87b716dc48f0277d): manifiesto, models/partner.py y models/res_country.py consultados; wizard y carga CSV no ejecutados.
- [stock_account_purchase legado](https://github.com/jeffrepo/stock_account_purchase/tree/a3594d2ac577c0c491933ca743de46fcf20fb160): manifiesto, modelos y vista revisados.

Los hashes identifican la fuente, no acreditan instalación ni equivalencia funcional Enterprise. Las consultas web a documentación ORM/JavaScript fallaron por timeout/acceso; se utilizó el código oficial de Odoo. La URL errónea `models/res_partner.py` del legado devolvió 404; el archivo correcto es `models/partner.py`.


## Seguimiento POS y direcciones

Se volvió a comparar el modelo CP y los related del legado en e3aed4a499c3617644d47afa87b716dc48f0277d. Para el port de cantidades se consultaron en Odoo 18 commit 54c0991d2949bf4090231c8c167b4a1038769085: pos_store.js (pay), payment_screen.js (validateOrder), models/pos_order.py (_process_saved_order/action_pos_order_paid), models/pos_load_mixin.py y views/pos_config_view.xml. El loader vacío significa todos los campos. Se confirmó que el core captura excepciones no SQL alrededor de action_pos_order_paid: por eso el guardia se sitúa fuera de ese try.

Se consultó res_partner.py del mismo commit: _address_fields controla la sincronización con hijos; el port incluye los vínculos y texto fiscal. No se portó el override legacy de vistas. La plantilla oficial OrderReceipt ya muestra customerNote; eso no demuestra que las notas históricas note estén migradas.

La ficha oficial sh_pos_order_list 18 estuvo disponible mediante búsqueda; la consulta directa de sh_pos_order_sync 18 recibió 429. La tienda de Softhealer confirma el producto, no el paquete instalado. Enlaces en SUPPLIER_REQUESTS.md. No se descargó código propietario.
