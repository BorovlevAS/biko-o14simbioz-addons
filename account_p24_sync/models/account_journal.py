# -*- coding: utf-8 -*-

import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    autoclient_id = fields.Char(
        string='Autoclient Id',
    )
    autoclient_token = fields.Char(
        string='Autoclient Token',
    )
    bank_sanitized_acc_number = fields.Char(
        string='Sanitized Account Number',
        related='bank_account_id.sanitized_acc_number',
        readonly=True,
        store=True)

    @api.model
    def _get_bank_statements_available_sources(self):
        bank_statements_source = super(AccountJournal, self)._get_bank_statements_available_sources()
        bank_statements_source.append(('p24_import', 'Privat24 Import'))
        return bank_statements_source

    def p24_sync_statement(self):
        autoclient_id = token = ''
        if not self.bank_acc_number:
            raise UserError(_('Provide "Account Number" on bank journal!'))
        if self.autoclient_id:
            autoclient_id = base64.b64decode(self.autoclient_id).decode('utf-8')
        if self.autoclient_token:
            token = base64.b64decode(self.autoclient_token).decode('utf-8')
        initial_values = {
            'journal_id': self.id,
            'bank_acc': self.bank_sanitized_acc_number,
            'state': 'success',
            'task': 'statement_import',
            'autoclient_id': autoclient_id,
            'autoclient_token': token,
        }

        p24 = self.env['account.p24.sync'].create(initial_values)
        return p24.do_sync()

    def write(self, vals):
        if vals.get('autoclient_id'):
            vals['autoclient_id'] = base64.b64encode(vals['autoclient_id'].encode('utf-8'))
        if vals.get('autoclient_token'):
            vals['autoclient_token'] = base64.b64encode(vals['autoclient_token'].encode('utf-8'))
        return super(AccountJournal, self).write(vals)

    @api.model
    def create(self, vals):
        if vals.get('autoclient_id'):
            vals['autoclient_id'] = base64.b64encode(vals['autoclient_id'].encode('utf-8'))
        if vals.get('autoclient_token'):
            vals['autoclient_token'] = base64.b64encode(vals['autoclient_token'].encode('utf-8'))
        return super(AccountJournal, self).create(vals)

    def read(self, fields=None, load='_classic_read'):
        data = super(AccountJournal, self).read(fields=fields, load=load)
        for vals in data:
            if vals.get('autoclient_id'):
                vals['autoclient_id'] = base64.b64decode(vals['autoclient_id']).decode('utf-8')
            if vals.get('autoclient_token'):
                vals['autoclient_token'] = base64.b64decode(vals['autoclient_token']).decode('utf-8')
        return data
