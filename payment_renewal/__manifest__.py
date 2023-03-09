# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Franchise Renewal Payment',
    'Author': "Aswanth krishnan",
    'version': '15.0.1.0.0',
    'summary': '',
    'description': """Renew Payment""",
    'category': '',
    'depends': ['raz_pay'],
    'data': [
        'data/renewal_cron.xml',
        'security/ir.model.access.csv',
        'views/renewal.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
