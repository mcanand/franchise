import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class EmControllers(http.Controller):

    @http.route('/gallery/', type='http', auth='public', website=True)
    def render_gallery(self, **args):
        return request.render("em_frontend.em_gallery")


    @http.route('/certifications/', type='http', auth='public', website=True)
    def render_certifications(self, **args):
        return request.render("em_frontend.em_certificates")