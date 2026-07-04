{
    "name": "Odoo AI Audit Security",
    "version": "18.0.1.0.0",
    "summary": "Read-only security for Odoo AI Audit Platform",
    "author": "AI Tech Pro",
    "license": "LGPL-3",
    "depends": ["base", "account", "point_of_sale", "stock", "product"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": False,
}