# -*- coding: utf-8 -*-
{
    'name': 'Franchise',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'Franchise Application',
    'description': """add website links and its categories""",
    'depends': ['base', 'country_locations', 'sale', 'product',
                'account', 'raz_pay', 'hide_menu_user', 'payment_renewal'],
    'data': [
        'security/ir.model.access.csv',
        'views/franchise_applications.xml',
        'views/menu.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/res_company.xml',
        'views/service_list.xml',
        'views/franchise_files.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/franchise_application/static/src/js/*.js',
            '/franchise_application/static/src/css/*.css',
        ],
        'web.assets_qweb': [
            '/franchise_application/static/src/xml/*.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
