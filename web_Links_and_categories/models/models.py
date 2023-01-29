from odoo import fields, models, api

class ProductCategory(models.Model):
    _inherit= 'product.category'

    icon = fields.Char(string='Icon')

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    link_url = fields.Text(string='Link url')


class FranchiseApplicationPartners(models.Model):
    _name = 'franchise.application.partner'
    _description = 'user application for franchise'

    application_sequence = fields.Char(string="Application Number", readonly=True, required=True, copy=False,
                                       default='New')
    name = fields.Char(string="Applicant Name")
    district_id = fields.Many2one('res.country.state.district', string="District")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    panchayat_id = fields.Many2one('res.country.state.district.panchayat', string="Panchayat")
    location = fields.Char(string="Location prefered")
    known_by = fields.Char(string="Known through")
    status = fields.Selection(
        [('draft', "Draft"), ('progress', 'In Progress'), ('done', 'Approved')], default='draft')
    color = fields.Integer('Color', compute='_get_color', store=True)

    @api.model
    def create(self, vals):
        if vals.get('application_sequence', 'New') == 'New':
            vals['application_sequence'] = self.env['ir.sequence'].next_by_code(
                'franchise.application.partner') or 'New'
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





