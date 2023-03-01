from odoo import fields, models, api, _


class PaymentAcquirerInherit(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(
        selection_add=[('razorpay', "razor pay")],
        ondelete={'razorpay': 'set default'})

    razorpay_endpoint = fields.Char(string="End point",
                                    required_if_provider='razorpay')
    razorpay_api_key = fields.Char(string="API key",
                                   required_if_provider='razorpay')
    razorpay_secret_key = fields.Char(string="Secret Key",
                                      required_if_provider='razorpay')
