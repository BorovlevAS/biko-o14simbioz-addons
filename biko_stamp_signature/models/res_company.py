from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    stamp_image = fields.Image(string="Stamp of company")