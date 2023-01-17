{
    'name': "Franchise Dashboard",
    'version': '15.0.0.1',
    'summary': """franchise user dashboard""",
    'description': """""",
    'author': 'ANAND MC',
    'depends': [],
    'data': [
        'views/franchise_dash.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/franchise_dashboard/static/src/js/dashboard.js',
            '/franchise_dashboard/static/src/css/main.scss',
        ],
        'web.assets_qweb': [
            '/franchise_dashboard/static/src/xml/dashboard.xml',
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
