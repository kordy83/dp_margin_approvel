# -*- coding: utf-8 -*-

{
    'name'        : 'Margin Approvel',
    'version'     : '17.0',
    "author"      : "Kordy",
    "support"     : "kordy.com",
    'category'    : 'account',
    'summary'     : '''This helps you to need to users Approvel based on margin approvel rule''',
    'description' : """ This helps you to need to users Approvel based on rule margin approvel rule""",
    'depends': ['base','sale_management', 'sale_margin'],
    'data'        : [
                    "security/ir.model.access.csv",
                    "security/margin_groups.xml",
                    "views/approval_view.xml",
                    "views/sales_view.xml",
                    ],
    'installable' : True,
    'auto_install': False,
    "price"       : 20,
    "currency"    : "EUR",
    "images"      : ["static/description/banner.png",],
}
