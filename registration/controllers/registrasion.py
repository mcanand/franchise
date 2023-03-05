import base64
import datetime
import json
import logging
import random
from ast import literal_eval

from dateutil.relativedelta import relativedelta
from odoo import SUPERUSER_ID, _, fields, http
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import exception_to_unicode

_logger = logging.getLogger(__name__)

# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error',
                          'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name',
                          'partner_id',
                          'password', 'confirm_password', 'city', 'country_id',
                          'lang', 'phone','renewal'}


class RegistrationController(http.Controller):
    @http.route('/franchise/applied', type="http", auth="public", website=True)
    def registration_redirect(self, **kwargs):
        template = 'registration.register_redirect_template'
        if kwargs:
            franchise = request.env['franchise.application.partner']
            details = franchise.search([('id', '=', kwargs.get('id'))])
            return request.render(template, {'details': details})
        return request.render(template)

    @http.route('/registration/franchise', type="http", auth="public",
                website=True)
    def registration_franchise(self, **args):
        """register franhchise application users"""
        if not args:
            district = request.env['res.country.state.district'].search([])
            value = {}
            value.update({
                "districts": district,
            })
            return request.render("registration.franchise_registration", value)
        referal_code = self.get_referal_code()
        get_ref = args.get("referd_by")
        application_id = request.env[
            'franchise.application.partner'].sudo().create({
            "name": args.get('name'),
            "dob": args.get('dob'),
            "renewal":args.get('renewal'),
            "email": args.get('email'),
            "mobile": args.get('phone'),
            "local_body": args.get('local_body'),
            "district_id": args.get('district'),
            "panchayat_id": args.get('panchayat'),
            "location": args.get('location'),
            "known_by": args.get('known_by'),
            "my_referal": referal_code,
            "referd_by": get_ref
        })
        val = application_id.id
        return request.redirect('/franchise/applied?id=%s' % val)

    def get_referal_code(self):
        """create referal code for users"""
        code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = ''
        for i in range(0, 8):
            slice_start = random.randint(0, len(code_chars) - 1)
            code += code_chars[slice_start: slice_start + 1]
        return code

    @http.route('/get/panchayats', type='json', auth="public")
    def get_panchayat(self, **kwargs):
        """
        select panchayath,municipality or corparation by checking selected
        district.
        """
        if kwargs.get('local_body') == 'panchayath':
            values = request.env[
                'res.country.state.district.panchayat'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        if kwargs.get('local_body') == 'municipality':
            values = request.env[
                'res.country.state.district.municipality'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        if kwargs.get('local_body') == 'corporation':
            values = request.env[
                'res.country.state.district.corparation'].sudo().search(
                [('district_id', '=', int(kwargs.get('district')))])
        datas = []
        for value in values:
            datas.append({'id': value.id, 'name': value.name})
        return datas

    @http.route('/check/user', type='json', auth="public")
    def user_checking(self, **args):
        """
        check user alredy exist or not
        """
        application_user = request.env['franchise.application.partner'].search(
            ['|', ('email', '=', args.get('email')),
             ('mobile', '=', args.get('phone'))]
        )
        if not application_user:
            return False
        return True

    @http.route('/check/referal', type='json', auth="public")
    def _check_referal(self, **args):
        """
        check user alredy exist or not
        """
        application_user = request.env['res.users'].search(
            [('reference', '=', args.get('referal'))]
        )
        if not application_user:
            return False
        return True
