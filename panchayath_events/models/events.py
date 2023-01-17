from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class PanchayathEvents(models.Model):
    _name = 'panchayath.events'
    _description = "Panchayath events"

    name = fields.Char(string="Event Name", required=True)
    district_id = fields.Many2one('res.country.state.district', string="District", required=True)
    panchayat_id = fields.Many2one('res.country.state.district.panchayat', string='panchayat', required=True)
    panchayath_assis = fields.Many2one('res.partner', string='Panchayath assistance', required=True)
    image = fields.Binary(string='image')
    schedule_date = fields.Datetime(string="Schedule Date", required=True)
    category = fields.Selection([('emergency', 'Emergency'), ('health', 'Health')],required=True)
    priority = fields.Integer(string='priority' ,required=True)
    heading =fields.Text(string="Heading", required=True)
    subheading =fields.Text(string="Sub heading", required=True)
    message =fields.Html(string="Message", required=True)
    state = fields.Selection([
        ('not_published', ' Not Published'),
        ('published', ' Published'),

    ], string='Status', default="not_published",readonly=True)


    @api.onchange('category')
    def onchange_age(self):
        self.priority = 2 if not self.category =='emergency' else 1

    def write(self, vals):
        res = super(PanchayathEvents,self).write(vals)
        if self.priority >1:
            raise ValidationError(('You should select at least one Advanced Presence Control option.'))

        return res

    def post(self):
        print("jh")
        if self.state == 'not_published':
            self.state = 'published'

    def cancel(self):
        print("sa")
        if self.state == 'published':
            self.state = 'not_published'









