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
    category = fields.Selection([('emergency', 'Emergency'), ('health', 'Health')], required=True)
    priority = fields.Integer(string='priority', required=True)
    heading = fields.Text(string="Heading", required=True)
    subheading = fields.Text(string="Sub heading", required=True)
    message = fields.Html(string="Message", required=True)
    state = fields.Selection([
        ('not_published', ' Not Published'),
        ('published', ' Published'),

    ], string='Status', default="not_published", readonly=True)

    @api.onchange('category')
    def onchange_age(self):
        self.priority = 2 if not self.category == 'emergency' else 1

    def write(self, vals):
        if self.priority > 1 and self.category == 'emergency':
            raise ValidationError(('Priority of emergency must be 1'))
        if self.priority == 0 and self.category == 'emergency':
            raise ValidationError(('Priority of emergency will not be equal to 0'))
        elif self.priority < 2 and self.category != 'emergency':
            raise ValidationError(('Priority of health will not be eqal to 1'))
        res = super(PanchayathEvents, self).write(vals)
        return res

    @api.model_create_multi
    def create(self, vals):
        res = super(PanchayathEvents, self).create(vals)
        if self.priority > 1 and self.category == 'emergency':
            raise ValidationError(('Priority of emergency must be 1'))
        if self.priority == 0 and self.category == 'emergency':
            raise ValidationError(('Priority of emergency will not be equal to 0'))
        elif self.priority < 2 and self.category != 'emergency':
            raise ValidationError(('Priority of health will not be eqal to 1'))
        # res = super(PanchayathEvents, self).create(vals)
        return res

    def post(self):
        print("jh")
        if self.state == 'not_published':
            self.state = 'published'

    def cancel(self):
        print("sa")
        if self.state == 'published':
            self.state = 'not_published'
