# -*- coding: utf-8 -*-
{
    'name': 'country extra locations',
    'version': '16.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'add districts, panchayats, Municipality, Corporation',
    'description': """add districts and panchayat for states""",
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/district.xml',
        'views/panchayat.xml',
        'views/corporation.xml',
        'views/municipality.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
