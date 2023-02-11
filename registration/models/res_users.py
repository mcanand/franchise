from odoo import fields, models


class ExtendUsers(models.Model):
    _inherit = ['res.users']

    reference = fields.Char(string="Reference Code")
