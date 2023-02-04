# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'franchise_panchayath_admin',
    'Author':"Aswanth krishnan",
    'version': '15.0.1.0.0',
    'summary': 'panchayath admin',
    'description': """register the users in emithram""",
    'category': '',
    'depends': ['website', 'District_Panchayat', 'web', 'muncipality_corparation', 'web_Links_and_categories'],
    'data': [
        'views/registration_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/registration/static/css/registration.css',
            '/registration/static/css/popup.css',
            '/registration/static/js/panchayath_selection.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
}
