from odoo import fields, models


class Municipality(models.Model):
    _name = 'res.country.state.district.municipality'
    _description = 'municipality of District'

    name = fields.Char(string="Municipality Name", required=True)
    code = fields.Char(string="Municipality Code")
    district_id = fields.Many2one('res.country.state.district', string="District", required=True)


class Corparation(models.Model):
    _name = 'res.country.state.district.corparation'
    _description = 'corparation of District'

    name = fields.Char(string="Corparation Name", required=True)
    code = fields.Char(string="Corparation Code")
    district_id = fields.Many2one('res.country.state.district', string="District", required=True)