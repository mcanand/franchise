{
    'name': 'EM front end',
    'description': 'front end design for e mitram',
    'category': '',
    'summary': '',
    'version': '15.0.0.1',
    'author': 'ANAND MC',
    'depends': ['website'],
    'data': [
        'views/home.xml',
        'views/gallery.xml',
        'views/certificates.xml',
    ],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'em_frontend/static/src/css/home.css',
        ],
    },
    'installable': True,
    'application': True,
}