import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number
import requests
import datetime
import json

import logging

_logger = logging.getLogger(__name__)

class P24BBankSyncPatch(models.TransientModel):
    _inherit = 'account.p24.sync'

    def _complete_stmts_vals(self, stmts_vals, journal, account_number):
        ResPB = self.env['res.partner.bank']
        res_partner_model = self.env['res.partner']
        for st_vals in stmts_vals:
            st_vals['journal_id'] = journal.id

            for line_vals in st_vals['transactions']:
                unique_import_id = line_vals.get('unique_import_id')
                if unique_import_id:
                    sanitized_account_number = sanitize_account_number(
                        account_number)
                    line_vals['unique_import_id'] = \
                        (sanitized_account_number and
                         sanitized_account_number + '-' or '') + \
                        str(journal.id) + '-' + unique_import_id

                if not line_vals.get('bank_account_id'):
                    # Find the partner and his bank account or create
                    # the bank account. The partner selected during the
                    # reconciliation process will be linked to the bank
                    # when the statement is closed.
                    bank_account_id = False
                    identifying_string = False

                    if line_vals.get('partner_edrpou'):
                        partner_id = res_partner_model.search([('enterprise_code', '=', line_vals['partner_edrpou']), ('is_company', '=', True)], limit=1)
                        if not partner_id:
                            partner_id = res_partner_model.create({
                                'name': line_vals['partner_name'],
                                'enterprise_code': line_vals['partner_edrpou'],
                                'is_company': True,
                            })
                        line_vals.pop('partner_edrpou')
                        line_vals['partner_id'] = partner_id.id

                    if line_vals.get('partner_acc'):
                        identifying_string = line_vals.get('partner_acc')
                    else:
                        identifying_string = line_vals.get('account_number')
                    if identifying_string:
                        partner_bank = ResPB.search(
                            [('acc_number', '=', identifying_string)], limit=1)
                        if partner_bank:
                            pass
                            # bank_account_id = partner_bank.id
                            # partner_id = partner_bank.partner_id.id
                        else:
                            if 'partner_acc' in line_vals and line_vals['partner_acc']:
                                bank_account_id = ResPB.create(
                                    {'acc_number': line_vals['partner_acc'],
                                     'partner_id': line_vals['partner_id']}).id
                            else:
                                bank_account_id = ResPB.create(
                                    {'acc_number': line_vals['account_number'],
                                     'partner_id': line_vals['partner_id'],
                                     }).id

                    line_vals['bank_account_id'] = bank_account_id
                    if 'partner_acc' in line_vals:
                        del line_vals['partner_acc']

        return stmts_vals

    def _do_send_payment(self):
        wiz_form_act = {
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'res_model': 'account.p24.sync',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
        recipient_bank = self.recip_bank
        headers = {
            'Content-Type': 'application/json; charset=cp1251',
            'token': self.autoclient_token,
            'id': self.autoclient_id,
            'User-Agent': 'клиентское приложение'.encode('utf-8')
        }

        data = {
            "document_number": str(self.id),
            "recipient_nceo": self.partner_id.enterprise_code,
            "payment_naming": self.partner_id.name,
            "payment_amount": '%.2f' % self.amount,
            "recipient_ifi": recipient_bank.bank_bic,
            "payment_destination": self.memo,
            "payer_account": self.bank_acc,
            "payment_ccy": "UAH"
        }
        if recipient_bank.is_card:
            data.update({
                'recipient_card': recipient_bank.acc_number
            })
        else:
            data.update({
                'recipient_account': recipient_bank.acc_number
            })
        try:
            response = self.s.post(self.url_payment, data=json.dumps(data), headers=headers, timeout=self.timeout)
        except Exception:
            _logger.info("Error in request: %s", response.text)
            raise UserError(_('Error in request'))

        if response.status_code == 201:
            # OK
            _logger.info("Response: OK")
            payment = self.env['account.payment'].search([('name', '=', self.document_number)])
            if payment:
                payment.is_exported = True
            self.state = 'success'
            return wiz_form_act
        elif response.status_code == 400:
            _logger.info("Error in response")
            resp_json = response.json()
            raise UserError(_('Error in response: %s' % resp_json))
        elif response.status_code == 401:
            self.state = 'loginpasswd'
            return wiz_form_act
        elif response.status_code == 403:
            _logger.info("Aoutoclient is disabled")
            raise UserError(_('Aoutoclient is disabled'))
        elif response.status_code in [503, 504]:
            _logger.info("Service is temporary unavailable")
            raise UserError(_('Service is temporary unavailable'))
        else:
            _logger.info('Can not send payment.')
            raise UserError(_('Can not send payment'))

    def do_sync_next(self):
        if not self.recip_bank.acc_number or not self.recip_bank.bank_name or not self.recip_bank.bank_bic or not self.recip_bank.bank_id.enterprise_code:
            raise UserError(_('Provide partner bank info!'))
        self.state = 'success'
        return self._do_sync()