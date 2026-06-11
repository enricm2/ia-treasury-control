{
    "name": "IA Treasury Control (MCP)",
    "version": "18.0.1.0.0",
    "summary": "Agente IA para tesorería, fiscal y facturas vía Claude MCP",
    "description": """
Conecta tu Odoo con Claude.ai para gestionar tesorería, fiscal y facturas
mediante lenguaje natural.

La lógica de los agentes se ejecuta de forma segura en los servidores de Uniasser.
Compatible con Odoo 16, 17, 18, 19 y Odoo.sh.

Requiere licencia SaaS: https://apps.uniasser.net
    """,
    "author": "Uniasser",
    "website": "https://apps.uniasser.net",
    "category": "Accounting/Accounting",
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "license": "OPL-1",
    "application": True,
    "installable": True,
    "auto_install": False,
}
