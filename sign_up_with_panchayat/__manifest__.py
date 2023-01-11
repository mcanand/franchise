# -*- coding: utf-8 -*-
{
    'name': 'Sign Up With Panchayat',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'signing up with district and panchayat',
    'description': """sign up with panchayat""",
    'depends': ['base', 'contacts', 'auth_signup', 'website', 'District_Panchayat'],
    'data': [
        'views/sign_up.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/sign_up_with_panchayat/static/src/js/change_country_filter.js',
            '/sign_up_with_panchayat/static/src/css/signup.css',
            '/sign_up_with_panchayat/static/src/css/login.css',
            '/sign_up_with_panchayat/static/src/css/reset_password.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
