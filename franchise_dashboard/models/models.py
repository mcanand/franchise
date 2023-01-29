from odoo import fields, models, api


class FranchiseDashboard(models.Model):
    _inherit = 'res.users'

    def get_values(self, **args):
        uid = self.env.user.id
        usr = self.browse(uid)
        user = {
            'id': usr.id,
            'name': usr.name,
            'email': usr.login,
            'phone': usr.mobile,
            'image': usr.image_1024,
            'panchayat': usr.panchayat_id.name
        }
        categ = self.env['product.category'].search([])
        categories = []
        for cat in categ:
            category = {'name': cat.name, 'id': cat.id, 'icon': cat.icon}
            categories.append(category)
        return user, categories

    def get_products(self, category_id):
        print(category_id)
        products = self.env['product.template'].search([('sale_ok', '=', True),
                                                        ('categ_id', '=', category_id)])
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
        return product_vals


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    def get_product_create_line(self, vals):
        """get product details and create order line for the current order"""
        product = self.env['product.template'].search([('id', '=', int(vals.get('product_id')))], limit=1)
        if product:
            self.env['sale.order.line'].create({'product_id': product.id, 'order_id': int(vals.get('order_id'))})
            vals = {
                'id': product.id,
                'name': product.name,
                'url': product.link_url,
                'image': product.image_1920,
                'categ': product.categ_id.name
            }
            return vals
        else:
            return False


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    active = fields.Boolean(string='active')

    def delete_current_order(self, order_id):
        """delete current sale order"""
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        order.unlink()
        return True

    def get_sale_order_details(self, vals):
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('id', '=', int(vals.get('order_id'))), ('user_id', '=', user_id)])
        partner = order.partner_id
        value = {}
        orders = {'id': order.id,
                  'order_name': order.name,
                  'amount_untaxed': order.amount_untaxed,
                  'amount_tax': order.amount_tax,
                  'amount_total': order.amount_total,
                  'c_name': partner.name,
                  'c_street': partner.street,
                  'c_street2': partner.street2,
                  'c_mobile': partner.mobile,
                  'c_zip': partner.zip}
        value['order'] = orders
        lines = []
        for rec in order.order_line:
            line = {'id': rec.id,
                    'product_name': rec.product_id.name,
                    'price': rec.price_unit,
                    'tax': rec.tax_id.name}
            lines.append(line)
        value['lines'] = lines
        return value

    def get_active_order(self):
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('active', '=', True), ('user_id', '=', user_id)], limit=1)
        if order:
            partner = order.partner_id
            value = {}
            orders = {'id': order.id,
                      'order_name': order.name,
                      'amount_untaxed': order.amount_untaxed,
                      'amount_tax': order.amount_tax,
                      'amount_total': order.amount_total,
                      'c_name': partner.name,
                      'c_street': partner.street,
                      'c_street2': partner.street2,
                      'c_mobile': partner.mobile,
                      'c_zip': partner.zip}
            value['order'] = orders
            lines = []
            for rec in order.order_line:
                line = {'id': rec.id,
                        'product_name': rec.product_id.name,
                        'price': rec.price_unit,
                        'tax': rec.tax_id.name}
                lines.append(line)
            value['lines'] = lines
            return value
        else:
            return False

    def confirm_order(self, order_id):
        user_id = self.env.user.id
        order = self.search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        if order:
            order.action_confirm()
            order.write({'active':False})
            invoice = order._create_invoices()
            invoice.action_post()
            return True
        else:
            return False


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def delete_order_line(self, line_id):
        line = self.search([('id', '=', int(line_id))])
        val = line.unlink()
        return True if val else False


class FranchiseCustomers(models.Model):
    _name = 'franchise.customers'

    # def save_user_details(self, vals):
    #     customer = self.env['res.partner'].create({'name': vals.get('name'),
    #                                                        'mobile': vals.get('mobile'),
    #                                                        'address': vals.get('address'),
    #                                                        'age': vals.get('age')
    #                                                        })
    #
    #     return {'id': customer.id} if customer else False
    #
    # def change_user_state(self, id):
    #     customer = self.env['res.partner'].browse(id)
    #     change = customer.write({'state': 'done'})
    #     return True if change else False
