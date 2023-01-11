# -*- coding: utf-8 -*-
{
    'name': 'Districts Panchayat',
    'version': '16.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'districts and panchayats',
    'description': """add districts and panchayat for states""",
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/district.xml',
        'views/panchayat.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
