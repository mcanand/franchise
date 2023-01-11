from odoo import models, fields, _
from odoo.http import request


class WebsiteInherit(models.Model):
    _inherit = 'website'

    def get_current_state(self):
        """get current state by geolocation and search state in database Todo"""
        state = self.env['res.country.state'].search([('name', '=', 'Kerala')], limit=1)
        return state

    def get_districts(self):
        state = self.get_current_state()
        districts = self.env['res.country.state.district'].search([('state_id', '=', state.id)])
        return districts


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    panchayat_admin = fields.Boolean(string='Panchayat Admin')
    panchayat_id = fields.Many2one('res.country.state.district.panchayat', string='Panchayt')
    district_id = fields.Many2one('res.country.state.district', string='District')


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    panchayat_admin = fields.Boolean(string='Panchayat Admin')
    panchayat_id = fields.Many2one('res.country.state.district.panchayat', string='Panchayt')
    district_id = fields.Many2one('res.country.state.district', string='District')
