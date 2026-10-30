{
    "name": "Require Product Quantity in POS",
    "version": "18.0.1.0.0",
    "summary": "Validate zero quantities before payment and on server finalization",
    "author": "Grupo Mi Pan, Coop IT Easy SCRLfs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": ["views/pos_config.xml"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_require_product_quantity/static/src/quantity_validation.js",
            "pos_require_product_quantity/static/src/payment_guard.js",
        ],
    },
    "installable": True,
    "auto_install": False,
}
