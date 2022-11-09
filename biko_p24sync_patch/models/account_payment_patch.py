from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64

class AccountPaymentP24(models.Model):
    _inherit = 'account.payment'

    def p24_payment_export(self):
        for rec in self:
            if rec.state == 'draft':
                rec.action_post()
            autoclient_id = ''
            autoclient_token = ''
            if not rec.journal_id.bank_acc_number:
                raise UserError(_('Provide account number on bank journal!'))
            if rec.journal_id.autoclient_id:
                autoclient_id = base64.b64decode(rec.journal_id.autoclient_id).decode('utf-8')
            if rec.journal_id.autoclient_token:
                autoclient_token = base64.b64decode(rec.journal_id.autoclient_token).decode('utf-8')
            if not rec.partner_id:
                raise UserError(_('Provide partner!'))
            if rec.name == 'Draft Payment':
                raise UserError(_('At first confirm payment!'))
            # if not rec.communication:
            #     raise UserError(_('Set purpose of payment!'))
            if not rec.partner_id.bank_ids:
                raise UserError(_('Provide partner bank!'))
            if not rec.partner_id.enterprise_code:
                raise UserError(_('Provide partner EDRPOU!'))
            if len(rec.partner_id.bank_ids) > 1:
                initial_values = {
                    'state': 'choose_acc',
                    'journal_id': rec.journal_id.id,
                    'bank_acc': rec.journal_id.bank_acc_number,
                    'task': 'send_payment',
                    'partner_id': rec.partner_id.id,
                    'amount': rec.amount,
                    'currency_id': rec.currency_id.id,
                    'payment_date': rec.date,
                    'memo': rec.name,
                    'autoclient_id': autoclient_id,
                    'autoclient_token': autoclient_token,
                    'document_number': rec.name
                }
                p24 = self.env['account.p24.sync'].create(initial_values)
                return p24.do_sync()
            bank = rec.partner_id.bank_ids[0]
            if not bank.acc_number or not bank.bank_name or not bank.bank_bic:
                raise UserError(_('Provide partner bank info!'))
            initial_values = {
                'journal_id': rec.journal_id.id,
                'bank_acc': rec.journal_id.bank_acc_number,
                'recip_bank': bank.id,
                'state': 'success',
                'task': 'send_payment',
                'partner_id': rec.partner_id.id,
                'amount': '%.2f' % rec.amount,
                'currency_id': rec.currency_id.id,
                'payment_date': rec.date,
                'memo': rec.name,
                'autoclient_id': autoclient_id,
                'autoclient_token': autoclient_token,
                'document_number': rec.name
            }

            p24 = self.env['account.p24.sync'].create(initial_values)
            p24.do_sync()
