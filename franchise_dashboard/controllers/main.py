import requests
import json

from odoo import http
from odoo.http import request


class SaveCustomerOrderCreation(http.Controller):
    @http.route('/save/customer/create/order', type='json', auth="user")
    def save_customer_create_order(self, vals):
        customer_id = self.create_customer(vals)
        product_url = request.env['product.product'].sudo().search(
            [('id', '=', int(vals.get('product_id')))]).link_url
        sale_order = request.env['sale.order'].sudo()
        order_line = request.env['sale.order.line'].sudo()
        active_order = sale_order.search([('active_order', '=', True)])
        if active_order:
            active_order.write({'active_order': False})
        if customer_id:
            order = sale_order.create(
                {'partner_id': customer_id, 'active_order': True})
            order_line.create({'product_id': int(vals.get('product_id')),
                               'order_id': order.id})
            return {'customer_id': customer_id, 'order_id': order.id,
                    'product_url': product_url}
        else:
            return False

    def create_customer(self, vals):
        contact = request.env['res.partner'].sudo()
        partner = contact.search([('mobile', '=', vals.get('mobile'))],
                                 limit=1)
        if partner:
            partner.write({'name': vals.get('name'),
                           'mobile': vals.get('mobile'),
                           'phone': vals.get('mobile'),
                           'street2': vals.get('street2'),
                           'street': vals.get('street')})
            return partner.id
        else:
            customer = contact.create({'name': vals.get('name'),
                                       'mobile': vals.get('mobile'),
                                       'phone': vals.get('mobile'),
                                       'street2': vals.get('street2'),
                                       'street': vals.get('street'),
                                       'type': 'invoice',
                                       'user_id': request.env.user.id
                                       })
            return customer.id if customer else False

    @http.route('/find/customer/address', type='json', auth="user")
    def find_customer_address(self, number):
        res_partner = request.env['res.partner'].sudo()
        partner = res_partner.search([('mobile', 'ilike', int(number))],
                                     limit=1)
        if partner:
            vals = {'name': partner.name,
                    'mobile': partner.mobile,
                    'street': partner.street,
                    'street2': partner.street2,
                    'email': partner.email}
            return vals
        else:
            return False
