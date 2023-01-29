import requests
import json

from odoo import http
from odoo.http import request


class SaveCustomerOrderCreation(http.Controller):
    @http.route('/save/customer/create/order', type='json', auth="user")
    def save_customer_create_order(self, vals):
        customer_id = self.create_customer(vals)
        product = request.env['product.template'].sudo()
        product_url = product.search([('id', '=', int(vals.get('product_id')))]).link_url
        sale_order = request.env['sale.order'].sudo()
        order_line = request.env['sale.order.line'].sudo()
        active_order = sale_order.search([('active', '=', True)])
        if active_order:
            active_order.write({'active':False})
        if customer_id:
            order = sale_order.create({'partner_id': customer_id, 'active': True})
            order_line.create({'product_id': int(vals.get('product_id')), 'order_id': order.id})
            return {'customer_id': customer_id, 'order_id': order.id, 'product_url': product_url}
        else:
            return False

    def create_customer(self, vals):
        contact = request.env['res.partner'].sudo()
        partner = contact.search([('mobile', '=', vals.get('mobile'))])
        if partner:
            return partner.id
        else:
            customer = contact.create({'name': vals.get('name'),
                                       'mobile': vals.get('mobile'),
                                       'phone': vals.get('mobile'),
                                       'zip': vals.get('zip'),
                                       'street2': vals.get('location'),
                                       'street': vals.get('street'),
                                       'type': 'invoice',
                                       })
            return customer.id if customer else False
