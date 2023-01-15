# -*- coding: utf-8 -*-
{
    'name': 'web links and categories',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'website links and categories',
    'description': """add website links and its categories""",
    'depends': ['District_Panchayat'],
    'data': [
        'security/ir.model.access.csv',
        'views/web_links.xml',
        'views/web_link_categories.xml',
        'views/franchise_applications.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
