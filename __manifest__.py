# -*- coding: utf-8 -*-
{
    'name': "Web client extended notification",

    'summary': """
        Web client extend with refresh and notifications""",

    'description': """
        Extending geocoder with reverse functionality
    """,

    'author': "Polimex Team",
    'website': "https://polimex.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['mail'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/user_notify_wiz.xml',
        'security/ir.model.access.csv'
    ],
    # only loaded in demonstration mode

}
