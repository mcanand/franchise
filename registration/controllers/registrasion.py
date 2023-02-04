import base64
import datetime
import json
import logging
from ast import literal_eval

from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID, _, fields, http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import exception_to_unicode

_logger = logging.getLogger(__name__)

# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'phone'}


class RegistrationController(http.Controller):
    @http.route('/registration/franchise', type="http", auth="public", website=True)
    def registration_franchise(self,  **args):
        if not args:
            district = request.env['res.country.state.district'].search([])
            value = {}
            value.update({
                "districts": district,
            })
            return request.render("registration.franchise_registration", value)
        request.env['franchise.application.partner'].sudo().create({
            "name": args.get('name'),
            "dob": args.get('dob'),
            "email": args.get('email'),
            "mobile": args.get('phone'),
            "local_body": args.get('local_body'),
            "district_id": args.get('district'),
            "panchayat_id": args.get('panchayat'),
            "location": args.get('location'),
            "known_by": args.get('known_by'),
        })

    @http.route('/get/panchayats', type='json', auth="public")
    def get_panchayat(self, **kwargs):
        if kwargs.get('local_body') == 'panchayath':
            values = request.env['res.country.state.district.panchayat'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        if kwargs.get('local_body') == 'municipality':
            values = request.env['res.country.state.district.municipality'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        if kwargs.get('local_body') == 'corporation':
            values = request.env['res.country.state.district.corparation'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        datas = []
        for value in values:
            datas.append({'id': value.id, 'name': value.name})
        return datas

    @http.route('/check/user', type='json', auth="public")
    def user_checking(self, **args):
        application_user = request.env['franchise.application.partner'].search(
            ['|', ('email', '=', args.get('email')), ('mobile', '=', args.get('phone'))]
        )
        if not application_user:
            return False
        return True



