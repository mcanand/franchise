import requests
import json

from odoo import http
from odoo.http import request
import base64


class SaveCustomerOrderCreation(http.Controller):
    @http.route('/save/customer/create/order', type='json', auth="user")
    def save_customer_create_order(self, vals):
        customer_id = self.create_customer(vals)
        product_url = request.env['product.product'].sudo().search(
            [('id', '=', int(vals.get('product_id'))), ('company_id', '=', request.env.company.id)]).link_url
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

    @http.route('/search/product', type='json', auth='user')
    def search_product(self, vals):
        categ_id = request.env['product.category'].sudo().search(
            [('id', '=', int(vals.get('category_id')))])
        products = request.env['product.product'].sudo().search(
            [('categ_id.id', '=', categ_id.id),
             ('name', 'ilike', vals.get('input_val')), ('company_id', '=', request.env.company.id)])
        product_vals = []
        for val in products:
            product = {
                'id': val.id,
                'name': val.name,
                'url': val.link_url,
                'image': val.image_1920,
                'categ': val.categ_id.name
            }
            product_vals.append(product)
        print(product_vals)
        return product_vals

    @http.route('/load/settings', type='json', auth="user")
    def load_settings(self):
        user_id = request.env.user.id
        user = request.env['res.users'].sudo().search_read(
            [('id', '=', user_id)])
        return user

    @http.route('/franchise/files', type='json', auth="user")
    def Load_download_files(self):
        files = request.env['franchise.files'].sudo().search_read([('company_id', '=', request.env.company.id)])
        return files

    @http.route('/file/download', type='json', auth="user")
    def download(self, file_id):
        return self.download_file(file_id)

    def download_file(self, file_id):
        files = request.env['franchise.files'].sudo().search(
            [('id', '=', int(file_id)),('company_id', '=', request.env.company.id)])
        result = base64.b64encode(files.file.read())
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        attachment_obj = request.env['ir.attachment'].sudo()
        attachment_id = attachment_obj.create(
            {'name': files.name, 'datas_fname': files.name, 'datas': result})
        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
        # url = str(base_url)+"web/content/?model=franchise.files&id="+str(files.id)+"&filename_field=file&field=file&download=true&name="+files.file,
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }
