from odoo import fields, models, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    icon = fields.Char(string='Icon')


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

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

    panchayat_admin = fields.Boolean(string='Panchayat Admin')
    panchayat_id = fields.Many2one('res.country.state.district.panchayat',
                                   string='Panchayt')
    district_id = fields.Many2one('res.country.state.district',
                                  string='District')
    reference = fields.Char(string="Reference Code")
    referd_by_id = fields.Many2one('res.users',
                                   string="Referenced By")


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
        [('draft', "Draft"), ('progress', 'In Progress'),
         ('done', 'Approved')], default='draft')
    color = fields.Integer('Color', compute='_get_color', store=True)
    local_body = fields.Selection(
        [("panchayath", "Panchayath"), (" municipality", "Municipality"),
         ("corporation", "Corporation")])
    my_referal = fields.Char()
    referd_by = fields.Char()

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
        print("h")
        if self.status == 'draft':
            self.status = 'progress'

    def approve(self):
        invoice = self.env.ref("account.group_account_manager")
        sale = self.env.ref("sales_team.group_sale_manager")
        action = self.env['ir.actions.actions'].browse(336)
        res_users = self.env['res.users'].create({
            'name': self.name,
            'login': self.mobile,
            'sel_groups_1_9_10': '1',
            'panchayat_admin': True,
            'district_id': self.district_id.id,
            'panchayat_id': self.panchayat_id.id,
            'reference': self.my_referal,
            'groups_id': [(4, invoice.id), (4, sale.id)],
            'action_id': action.id,
        })
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
