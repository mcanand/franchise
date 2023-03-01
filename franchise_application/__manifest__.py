# -*- coding: utf-8 -*-
{
    'name': 'Franchise',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'website links and categories',
    'description': """add website links and its categories""",
    'depends': ['base', 'country_locations', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/franchise_applications.xml',
        'views/menu.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/res_company.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
