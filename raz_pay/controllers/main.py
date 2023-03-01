import logging
import pprint

import requests
from werkzeug import urls
from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class CashFreeController(http.Controller):
    _return_url = '/payment/razorpay/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False,
        save_session=False
    )
    def cashfree_return_from_checkout(self, **pdt_data):
        # print(pdt_data)
        # {'razorpay_payment_id': 'pay_LLvIaGyHLOmLT1',
        #  'razorpay_payment_link_id': 'plink_LLvDyAPPEnOebO',
        #  'razorpay_payment_link_reference_id': '',
        #  'razorpay_payment_link_status': 'paid',
        #  'razorpay_signature': '1b39604b0bd3ff1378f94743627d15ab91fbe40338732ddb027120a06d02b3c6'}
        _logger.info("handling redirection from razorpay with data:\n%s",
                     pprint.pformat(pdt_data))
        """pt data link id will come"""
        if not pdt_data:
            pass
        if pdt_data:
            # ''plink_LLxjLZB18ybSkB''
            details = request.env['payment.details'].sudo().search(
                [('razor_pay_id', '=', pdt_data['razorpay_payment_link_id'])],
                limit=1)
            if details.franchise_application_id.status != 'done':
                details.franchise_application_id.approve()
            else:
                return request.redirect('/')
        return request.redirect('/')
