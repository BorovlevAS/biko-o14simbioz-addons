from odoo import fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def name_get(self):
        return [(this.id, f'{this.acc_number} ({this.bank_name})') for this in self]