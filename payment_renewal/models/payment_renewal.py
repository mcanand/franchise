from datetime import date, datetime, timedelta
from odoo import fields, models, api, _


class PaymentRenewal(models.Model):
    _name = "payment.renewal"

    name = fields.Char(string="Name")
    user_id = fields.Many2one('res.users', string='User')

    renewal = fields.Selection([('month', 'Monthly'), ('year', 'Yearly')],
                               default="month")
    payment_success_date = fields.Datetime(string='payment success Date')
    renewal_date = fields.Date(string='Next renewal date')
    # razor_pay_id = fields.Char(string="Raz Payment Id")
    state = fields.Selection(
        [('cancel', 'Canceled'), ('pending', 'Pending'), ('send', 'Link Send'),
         ('paid', 'Paid')],
        default="month")

    def set_send(self):
        self.write({'state': 'send'})
        return True if self.state == 'send' else False

    def set_paid(self):
        self.write({'state': 'paid'})
        return True if self.state == 'paid' else False

    def _run_renew_payment(self):
        """check the renewal date"""
        print("minut")
        renewal = self.env['payment.renewal'].search(
            [('state', '=', 'pending')])
        print(renewal)
        for renewal in renewal:
            print(renewal.renewal_date)
            if date.today() < renewal.renewal_date:
                renewal.application_partner_id.send_payment_link()
                renewal.set_send()
                self.archive_user(renewal.user_id.id)

    def prepare_renewal_vals(self, record):
        """preparing values to create renewal"""
        vals = {
            'name': record.name,
            'payment_success_date': date.today(),
            'renewal': record.renewal,
            'user_id': record.related_users_id.id,
            'renewal_date': self.get_renewal_date(record),
            'state': 'pending',
        }
        return vals

    def create_renewal_record(self, details):
        """create rewal record for application for franchise"""
        application_id = details.franchise_application_id.id
        application_partner = self.env['franchise.application.partner']
        partner = application_partner.search([('id', '=', application_id)])
        vals = self.prepare_renewal_vals(partner)
        vals.update({'payment_details_id': details.id})
        renewal = self.create(vals)
        renewal.write({'application_partner_id': int(application_id)})
        if renewal:
            self.un_archive_user(renewal.user_id.id)
        return renewal if renewal else False

    def archive_user(self, user_id):
        """archive a user in res_users"""
        res_user = self.env['res.users']
        user = res_user.search([('id', '=', user_id)])
        user.write({'active': False})
        return True if not user.active else False

    def un_archive_user(self, user_id):
        """unarchive user in res_users"""
        res_user = self.env['res.users']
        user = res_user.search([('id', '=', user_id)])
        user.write({'active': True})
        return True if user.active else False

    def get_renewal_date(self, application_partner):
        """return renewal date by month oru by year"""
        if application_partner.renewal == 'month':
            next_month = datetime.now() + timedelta(days=30, hours=12,
                                                    minutes=00, seconds=00)
            return next_month
        else:
            next_year = datetime.now() + timedelta(days=365, hours=12,
                                                   minutes=00, seconds=00)
            return next_year
