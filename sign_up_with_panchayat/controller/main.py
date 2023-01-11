import logging
import werkzeug

from odoo import http, models, fields, _
from odoo.http import request, SessionExpiredException
from odoo.addons.auth_signup.controllers.main import ensure_db, AuthSignupHome
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class GetPanchayatSignUp(http.Controller):
    @http.route('/get/panchayats', type='json', auth="public")
    def get_panchayat(self, district):
        print(district, '3434')
        panchayat = request.env['res.country.state.district.panchayat'].sudo().search(
            [('district_id', '=', int(district))])
        panchayats = []
        for panchayat in panchayat:
            panchayats.append({'id': panchayat.id,
                               'name': panchayat.name})
        print(panchayats)
        return panchayats


class AuthSignupHomeInherit(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        qcontext.update({'district_id':kw.get('district_id'),
                         'panchayat_id':kw.get('panchayat_id')})
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                               raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
