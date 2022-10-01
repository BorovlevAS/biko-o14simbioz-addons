from odoo import fields, models

class Lead(models.Model):

    _inherit = 'crm.lead'

    inner_source_id = fields.Many2one(comodel_name = 'biko.source', string = 'Source (QDES)')
    lost_reason_comment = fields.Char(string = 'Lost reason (comment)')