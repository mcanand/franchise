# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'franchise_municipality_corparation',
    'Author':"Aswanth krishnan",
    'version': '15.0.1.0.0',
    'summary': 'municipality corparation',
    'description': """register the users in emithram""",
    'category': '',
    'depends': ['website', 'web', 'contacts'],
    'data': [
        "views/municipality.xml",
        "security/ir.model.access.csv",
        "views/corporation.xml",
    ],
    'assets': {
        'web.assets_frontend': [

        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
}