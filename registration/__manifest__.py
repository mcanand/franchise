# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Franchise Registration',
    'Author':"Aswanth krishnan",
    'version': '15.0.1.0.0',
    'summary': 'panchayath admin',
    'description': """register a franchise in emithram(form)""",
    'category': '',
    'depends': ['website', 'country_locations', 'web', 'franchise_application'],
    'data': [
        'views/registration_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/registration/static/css/registration.css',
            '/registration/static/css/popup.css',
            '/registration/static/js/registration.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
}
