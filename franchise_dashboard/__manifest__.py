{
    'name': "Franchise Dashboard",
    'version': '15.0.0.1',
    'summary': """franchise user dashboard""",
    'description': """""",
    'author': 'ANAND MC',
    'depends': ['base', 'contacts', 'sale'],
    'data': [
        'views/franchise_dash.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/franchise_dashboard/static/src/js/*.js',
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap',
            '/franchise_dashboard/static/src/css/*.css',
        ],
        'web.assets_qweb': [
            '/franchise_dashboard/static/src/xml/dashboard.xml',
            '/franchise_dashboard/static/src/xml/settings.xml',
        ],
    },
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
