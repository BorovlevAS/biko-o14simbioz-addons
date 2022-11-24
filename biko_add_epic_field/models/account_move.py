from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    biko_epic = fields.Char(string="EPIC")