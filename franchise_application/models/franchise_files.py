from odoo import fields, models, api


class FranchiseDashboard(models.Model):
    _name = 'franchise.files'

    name = fields.Char(string="Name")
    file = fields.Binary(string="Files")
    company_id = fields.Many2one('res.company')