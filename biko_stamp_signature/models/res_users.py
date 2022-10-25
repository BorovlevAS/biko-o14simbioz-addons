from odoo import fields, models

class Users(models.Model):
    _inherit = 'res.users'

    stamp_image = fields.Image(string="Personal signature")