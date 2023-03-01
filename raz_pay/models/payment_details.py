from odoo import fields, models, api, _
import razorpay


class PaymentTransactionInherit(models.Model):
    _name = 'payment.details'

    franchise_application_id = fields.Many2one('franchise.application.partner',
                                               string="franchise application", )
    acquirer_id = fields.Many2one('payment.acquirer', string="acquirer")
    payment_link = fields.Char(string="payment link")
    razor_pay_id = fields.Char(string="razor pay id")
    email = fields.Char(string="email")
    mobile = fields.Char(string="mobile")
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                             default='draft')

    @api.onchange('franchise_application_id')
    def onchange_application_id(self):
        """onchange application id in the field email and mobile number
        fields will be filled with franchise email and mobile number"""
        vals = {'email': self.franchise_application_id.email,
                'mobile': self.franchise_application_id.mobile, }
        self.write(vals)

    def create_payment_link(self, vals):
        acquirer = self.get_acquirer(vals)
        vals['acquirer_id'] = acquirer.id
        details = self.create_payment_detail(vals)
        if details:
            vals = {'api_key': details.acquirer_id.razorpay_api_key,
                    'secret_key': details.acquirer_id.razorpay_secret_key,
                    'amount': self.get_renew_amount(details),
                    'eamil': details.franchise_application_id.email,
                    'mobile': details.franchise_application_id.mobile,
                    'name': details.franchise_application_id.name,
                    'call_back_url': self.get_base_url_new() + "/payment/razorpay/return"}
            response = self.create_razorpay_link(vals)
            details.write({'razor_pay_id': response['id'],
                           'payment_link': response['short_url']})
            return True
        return False

    def get_renew_amount(self, details):
        company = self.env.company
        if details.franchise_application_id.renewal == 'month':
            amount = company.month_renew_amount
            return amount
        elif details.franchise_application_id.renewal == 'year':
            amount = company.year_renew_amount
            return amount

    def get_base_url_new(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    def create_razorpay_link(self, vals):
        client = razorpay.Client(
            auth=(vals.get('api_key'), vals.get('secret_key')))
        response = client.payment_link.create({
            "amount": int(vals.get('amount')) * 100,
            "currency": "INR",
            "accept_partial": False,
            "first_min_partial_amount": 0,
            "description": "Franchise Application Payment",
            "customer": {
                "name": vals.get('name'),
                "email": vals.get('email'),
                "contact": "+91" + vals.get('mobile')
            },
            "notify": {
                "sms": True,
                "email": True,
                "Whatsapp": True
            },
            "reminder_enable": True,
            "options": {
                "checkout": {
                    "theme": {
                        "hide_topbar": True
                    },
                    "name": self.env.company.name,
                    "method": {
                        "netbanking": "1",
                        "card": "1",
                        "upi": "1",
                        "wallet": "0"
                    }
                }
            },
            "notes": {
                "policy_name": "E-mitram Franchise Register"
            },
            "callback_url": vals.get('call_back_url'),
            "callback_method": "get"

        })
        return response

    def get_acquirer(self, vals):
        """get payment acquirer"""
        acquirer = self.env['payment.acquirer']
        acquirer = acquirer.search([('provider', '=', vals.get('acquirer'))])
        return acquirer

    def create_payment_detail(self, vals):
        """create a payment transaction"""
        val = {'franchise_application_id': vals.get('application_id'),
               'acquirer_id': vals.get('acquirer_id')}
        details = self.env['payment.details'].create(val)
        return details if details else False
