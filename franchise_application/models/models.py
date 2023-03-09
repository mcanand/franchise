from odoo import fields, models, api, _


class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    month_renew_amount = fields.Float(string="Monthly Renewal Amount(RS)")
    year_renew_amount = fields.Float(string="Yearly Renewal Amount(RS)")


class ProductCategory(models.Model):
    _inherit = 'product.category'

    icon = fields.Char(string='Icon')


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    link_url = fields.Text(string='Link url')


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    link_url = fields.Text(string='Link url')


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    panchayat_admin = fields.Boolean(string='Panchayat Admin')
    panchayat_id = fields.Many2one('res.country.state.district.panchayat',
                                   string='Panchayt')
    district_id = fields.Many2one('res.country.state.district',
                                  string='District')


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    local_body = fields.Selection(
        [("panchayath", "Panchayath"), (" municipality", "Municipality"),
         ("corporation", "Corporation")])
    panchayat_admin = fields.Boolean(string='Panchayat Admin')
    panchayat_id = fields.Many2one('res.country.state.district.panchayat',
                                   string='Panchayt')
    municipality_id = fields.Many2one(
        'res.country.state.district.municipality', string="Municipality")
    corporation_id = fields.Many2one('res.country.state.district.corporation',
                                     string="Corporation")
    district_id = fields.Many2one('res.country.state.district',
                                  string='District')
    reference = fields.Char(string="Reference Code", readonly=True)
    referd_by_id = fields.Many2one('res.users',
                                   string="Referenced By")


class InheritPaymentDetails(models.Model):
    _inherit = 'payment.details'



class InheritPaymentRenewal(models.Model):
    _inherit = 'payment.renewal'

    application_partner_id = fields.Many2one('franchise.application.partner',
                                             string='Application Partner')
    payment_details_id = fields.Many2one('payment.details',
                                         string="Payment Detail")


class FranchiseApplicationPartners(models.Model):
    _name = 'franchise.application.partner'
    _description = 'user application for registration'

    application_sequence = fields.Char(string="Application Number",
                                       readonly=True, required=True,
                                       copy=False,
                                       default='New')
    name = fields.Char(string="Applicant Name")
    district_id = fields.Many2one('res.country.state.district',
                                  string="District")
    dob = fields.Date(string="Date of Birth", required=True)
    related_users_id = fields.Many2one('res.users', string="Related Users")
    age = fields.Integer(string="AGE", store=True)
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    panchayat_id = fields.Many2one('res.country.state.district.panchayat',
                                   string="Panchayat")
    location = fields.Char(string="Location prefered")
    known_by = fields.Char(string="Known through")
    status = fields.Selection(
        [('draft', "Draft"), ('progress', 'In Progress'), ('paid', 'Paid'),
         ('done', 'Approved')], default='draft')
    color = fields.Integer('Color', compute='_get_color', store=True)
    local_body = fields.Selection(
        [("panchayath", "Panchayath"), (" municipality", "Municipality"),
         ("corporation", "Corporation")])
    my_referal = fields.Char()
    referd_by = fields.Char()
    payment_link = fields.Char(string="payment link")
    renewal = fields.Selection([('month', 'Monthly'), ('year', 'Yearly')],
                               default="month")
    payment_details_ids = fields.One2many('payment.details',
                                          'franchise_application_id',
                                          string="Payment Details")
    payment_renewal_ids = fields.One2many('payment.renewal',
                                          'application_partner_id',
                                          string="Payment Renewal")

    @api.model
    def create(self, vals):
        if vals.get('application_sequence', _('New')) == _('New'):
            vals['application_sequence'] = self.env[
                                               'ir.sequence'].next_by_code(
                'franchise.application.partner') or _('New')
        result = super(FranchiseApplicationPartners, self).create(vals)
        return result

    @api.depends('status')
    def _get_color(self):
        for rec in self:
            if rec.status == 'draft':
                rec.color = 9
            elif rec.status == 'progress':
                rec.color = 7
            elif rec.status == 'done':
                rec.color = 10

    def check(self):
        if self.status == 'draft':
            self.status = 'progress'

    def send_payment_link(self):
        vals = {'application_id': self.id,
                'acquirer': 'razorpay'}
        pay_link = self.env['payment.details'].create_payment_link(vals)
        if pay_link:
            print('done')

    def hide_menus(self, res_users):
        menus = []
        menus.append(self.env.ref('base.menu_management').id)
        menus.append(self.env.ref('franchise_application.menu_franchisee').id)
        menus.append(self.env.ref('contacts.menu_contacts').id)
        menus.append(self.env.ref('sale.sale_menu_root').id)
        menus.append(self.env.ref('account.menu_finance').id)
        menus.append(self.env.ref('website.menu_website_configuration').id)
        menus.append(self.env.ref('utm.menu_link_tracker_root').id)
        menus.append(self.env.ref('base.menu_administration').id)
        for rec in menus:
            res_users.write({'hide_menu_ids': [(4, rec)]})

    def approve(self):
        invoice = self.env.ref("account.group_account_manager")
        sale = self.env.ref("sales_team.group_sale_manager")
        action = self.env['ir.actions.actions'].search(
            [('name', '=', 'Franchise Dashboard')])
        res_users = self.env['res.users'].create({
            'name': self.name,
            'login': self.email,
            'email': self.email,
            'sel_groups_1_9_10': '1',
            'panchayat_admin': True,
            'local_body': self.local_body,
            'district_id': self.district_id.id,
            'panchayat_id': self.panchayat_id.id,
            'reference': self.my_referal,
            'groups_id': [(4, invoice.id), (4, sale.id)],
            'action_id': action.id,
        })
        if res_users:
            self.hide_menus(res_users)
        if self.referd_by:
            referense_user = self.env['res.users'].search(
                [('reference', '=', self.referd_by)]
            )
            res_users.write({
                'referd_by_id': referense_user.id,
            })
        self.write({'related_users_id': res_users.id})
        if self.status == 'progress':
            self.status = 'done'

    def cancel(self):
        if self.status == 'done':
            self.status = 'draft'


class PaymentDetailsInherit(models.Model):
    _inherit = 'payment.details'

    franchise_application_id = fields.Many2one('franchise.application.partner',
                                               string="franchise application")
