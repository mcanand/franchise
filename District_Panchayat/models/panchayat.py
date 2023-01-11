from odoo import fields, models


class Districts(models.Model):
    _name = 'res.country.state.district.panchayat'
    _description = 'districts of state'

    name = fields.Char(string="Panchayat Name", required=True)
    code = fields.Char(string="Panchayat Code", required=True)
    district_id = fields.Many2one('res.country.state.district', string="District", required=True)
