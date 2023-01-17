# -*- coding: utf-8 -*-
{
    'name': 'Panchyat Events',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'AMRITA MS',
    'summary': 'panchayath events',
    'description': """""",
    'depends': ['base', 'contacts'],
    'data': [

        'security/ir.model.access.csv',
        'views/events.xml',


    ],
    'web.assets_backend': [
            'panchayath_events/static/src/css/image.css',
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}