from odoo import fields, models, api


class FranchiseDashboard(models.Model):
    _name = 'franchise.dashnoard'

    def get_value(self):
        return True
