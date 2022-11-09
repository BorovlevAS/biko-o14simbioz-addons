import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def __get_bank_statements_available_sources(self):
        bank_statements_source = super(AccountJournal, self).__get_bank_statements_available_sources()
        bank_statements_source.append(('p24_import', 'Privat24 Import'))
        return bank_statements_source