from odoo import http
from odoo.http import request
from datetime import date, datetime, timedelta


class AdminDashboardFranchise(http.Controller):
    @http.route('/admin/dashboard/values', type='json', auth="user")
    def save_customer_create_order(self, **kwargs):
        franchise = request.env['franchise.application.partner'].sudo()
        active_franchise = len(franchise.search([('status', '=', 'done')]))
        inactive_franchise = len(franchise.search([('status', '=', 'inactive')]))
        renewals = request.env['payment.renewal'].sudo()
        future_date = date.today() + timedelta(days=3)
        renew_in_3 = len(renewals.search([('renewal_date','<',future_date),('renewal_date','>',date.today()),('state','=','pending')]))
        vals = {'active_franchise': active_franchise,
                'inactive_franchise': inactive_franchise,
                'renew_in_3': renew_in_3}
        return vals

    @http.route('/admin/dah/table', type='json', auth='user')
    def get_table_values(self, val):
        franchise = request.env['franchise.application.partner'].sudo()
        if val == 'active':
            return franchise.search_read([('status', '=', 'done')])
        if val == 'inactive':
            return franchise.search_read([('status', '=', 'inactive')])
        if val == 'renewal':
            future_date = date.today() + timedelta(days=3)
            return franchise.search_read([('payment_renewal_ids.renewal_date', '<', future_date),
                             ('payment_renewal_ids.renewal_date', '>', date.today()),
                             ('payment_renewal_ids.state', '=', 'pending')])
