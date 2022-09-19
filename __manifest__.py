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
        'views/user_notify_wiz.xml',
        'views/res_users_demo.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'web_notify_extend/static/src/js/**/*',
        ],
        # 'web.tests_assets': [
        #     'web_notify_extend/static/tests/**/*',
        # ],
        # 'web.assets_qweb': [
        #     'web_notify_extend/static/src/xml/**/*',
        # ],
    },
    'license': 'LGPL-3',
    # only loaded in demonstration mode

}
