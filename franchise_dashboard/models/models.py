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
        products = self.env['product.product'].search([('sale_ok', '=', True),
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
        product = self.env['product.product'].search([('id', '=', int(vals.get('product_id')))], limit=1)
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

    active_order = fields.Boolean(string='active')

    def delete_current_order(self, order_id):
        """delete current sale order"""
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        order.unlink()
        return True

    def get_sale_order_details(self, vals):
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('id', '=', int(vals.get('order_id'))), ('user_id', '=', user_id)])
        value = {}
        if order:
            orders = self.get_order_vals(order)
            value['order'] = orders
            invoice_vals = self.get_invoice_vals(order)
            value['invoice'] = invoice_vals
            if order.order_line:
                lines = self.get_order_lines(order)
                print(lines)
                value['lines'] = lines
            return value
        else:
            return False

    def get_invoice_vals(self, order):
        invoice = order.invoice_ids
        return {'id': invoice.id if invoice else False,
                'pay_state': invoice.payment_state if invoice else 'draft',
                'html': invoice.get_portal_url(report_type='html') if invoice else False,
                'download_url': invoice.get_portal_url(report_type='pdf', download=True) if invoice else False,
                'print_url': invoice.get_portal_url(report_type='pdf') if invoice else False}

    def get_order_vals(self, order):
        partner = order.partner_id
        return {'id': order.id,
                'state': order.state,
                'order_name': order.name,
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_total,
                'c_name': partner.name,
                'c_street': partner.street,
                'c_street2': partner.street2,
                'c_mobile': partner.mobile,
                'c_zip': partner.zip}

    def get_order_lines(self, order):
        lines = []
        for rec in order.order_line:
            line = {'id': rec.id,
                    'product_name': rec.product_id.name,
                    'price': rec.price_unit,
                    'tax': rec.tax_id.name}
            lines.append(line)
        return lines

    def get_total_customers(self):
        user_id = self.env.user.id
        customers = self.env['res.partner'].search([('user_id','=',user_id)])
        return len(customers)

    def get_total_orders(self):
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('user_id','=',user_id)])
        return len(order)

    def get_active_order(self):
        user_id = self.env.user.id
        order = self.env['sale.order'].search([('active_order', '=', True), ('user_id', '=', user_id)], limit=1)
        value = {}
        value['total_customers'] = self.get_total_customers()
        value['total_service'] = self.get_total_orders()
        if order:
            orders = self.get_order_vals(order)
            value['order'] = orders
            invoice_vals = self.get_invoice_vals(order)
            value['invoice'] = invoice_vals
            if order.order_line:
                lines = self.get_order_lines(order)
                print(lines)
                value['lines'] = lines
            else:
                value['lines'] = False
            return value
        else:
            value['order'] = False
            value['invoice'] = False
            value['lines'] = False
            return value

    def confirm_order(self, order_id):
        user_id = self.env.user.id
        order = self.search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        if order:
            order.action_confirm()
            if order.invoice_ids:
                order.invoice_ids.button_draft()
                order.invoice_ids.unlink()
                invoice = order._create_invoices()
                invoice.action_post()
            else:
                invoice = order._create_invoices()
                invoice.action_post()
            return True
        else:
            return False

    def order_cancel(self, order_id):
        user_id = self.env.user.id
        order = self.search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        if order:
            order.action_cancel()
            return True
        return False

    def order_set_quotation(self, order_id):
        user_id = self.env.user.id
        order = self.search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        if order:
            order.action_draft()
            return True
        return False

    def complete_order(self,order_id):
        user_id = self.env.user.id
        order = self.search([('id', '=', int(order_id)), ('user_id', '=', user_id)])
        order.write({'active_order': False})
        return True

    def get_values(self, val):
        user_id = self.env.user.id
        print(val)
        if val == 'partner':
            partners = self.env['res.partner'].search_read([('user_id', '=', user_id)])
            return partners
        elif val == 'sales':
            sales = self.env['sale.order'].search_read([('user_id', '=', user_id)])
            return sales
        elif val == 'invoice':
            invoices = self.env['account.move'].search_read([('invoice_user_id', '=', user_id)])
            return invoices
        else:
            return False

    def get_sale_order_lines(self,order_id):
        lines = self.env['sale.order.line'].search_read([('order_id','=',int(order_id))])
        return lines


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def order_paid(self, invoice_id):
        invoice = self.env['account.move'].search([('id', '=', int(invoice_id))])
        if invoice.payment_state != 'paid':
            journal_id = self.env['account.journal'].search([('type', '=', 'bank')]).id
            vals = {'journal_id': journal_id,
                    'amount': invoice.amount_total,
                    'payment_date': invoice.invoice_date,
                    'communication': invoice.name}
            payment_register = self.env['account.payment.register']
            payments = payment_register.with_context(active_model='account.move', active_ids=invoice.id).create(
                vals)._create_payments()
            invoice.write({'payment_state': 'paid'})
            return True
        return False


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def delete_order_line(self, line_id):
        line = self.search([('id', '=', int(line_id))])
        val = line.unlink()
        return True if val else False


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    def update_partner(self, vals, customer_id):
        partner = self.env['res.partner'].search([('id', '=', int(customer_id))])
        return True if partner.write(vals) else False
