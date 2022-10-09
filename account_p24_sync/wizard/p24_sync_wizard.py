# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number
import requests
import datetime
import json

import logging

_logger = logging.getLogger(__name__)


class P24BBankSync(models.TransientModel):
    _name = 'account.p24.sync'
    _description = 'Privat24 Sync client'

    ######################################################
    # Privat24 part###############################
    ######################################################

    P24_STATEMENTS_URL = 'https://api.privatbank.ua/p24api/rest_fiz'
    P24_NEWPAYMENT_URL = 'https://api.privatbank.ua/p24api/pay_ua'

    balance_url = 'https://api.privatbank.ua/p24api/balance'

    url_transactions = "https://acp.privatbank.ua/api/proxy/transactions"
    url_balance = "https://acp.privatbank.ua/api/proxy/rest"
    url_payment = "https://acp.privatbank.ua/api/proxy/payment/create_pred"

    # Reusable session
    s = requests.Session()

    ######################################################
    # Odoo part ##########################################
    ######################################################
    state = fields.Selection(
        selection=[
            ('loginpasswd', 'Priovide Autoclient ID and Autoclient Token'),
            ('failure', 'Failure'),
            ('success', 'Success'),
            ('date_choose', 'Choose import date'),
            ('choose_acc', 'Choose supplier account'),
        ],
        string="State to control wizard form",
        default='loginpasswd')
    import_variant = fields.Selection(
        [('today', 'For today'),
         ('yesterday', 'For yesterday'),
         ('date_interval', 'For the date range')],
        default='today',
        string="Import date")
    start_import_date = fields.Date('Start import date')
    end_import_date = fields.Date('End import date')
    task = fields.Selection(
        [('nothing', 'Nothing to do'),
         ('statement_import', 'Import Statement'),
         ('send_payment', 'Send Payment')],
        default='nothing',
        string="Task to sync with bank eg statement or Payment")

    timeout = fields.Integer(
        string='Network delay in sec before exception',
        default=30,
    )
    autoclient_id = fields.Char(
        string='Autoclient ID',
        help='Autoclient ID',
        states={'loginpasswd': [('required', True)]})
    autoclient_token = fields.Char(
        string='Token',
        help='Autoclient Token',
        states={'loginpasswd': [('required', True)]})

    # Payment export
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='partner_id.company_id',
        readonly=True,
        store=True
    )
    memo = fields.Char(
        string='Memo'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
    )
    amount = fields.Monetary(
        string='Payment Amount',
    )
    payment_date = fields.Date(
        string='Payment Date',
    )

    recip_bank = fields.Many2one(
        comodel_name='res.partner.bank',
        domain="[('company_id', '=', company_id)]",
        string='Supplier bank account'
    )

    # task == 'statement_import' specific fields
    bank_acc = fields.Char(
        string='Bank Account Number',
        readonly=True
    )
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        help='Bank Journal for statement import'
    )
    document_number = fields.Char(
        string='Document number'
    )

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
                        partner_id = res_partner_model.search([('company_registry', '=', line_vals['partner_edrpou']), ('is_company', '=', True)], limit=1)
                        if not partner_id:
                            partner_id = res_partner_model.create({
                                'name': line_vals['partner_name'],
                                'company_registry': line_vals['partner_edrpou'],
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

    def _create_bank_statements(self, stmts_vals):
        """Create new bank statements from imported values.

        Filtering out already imported transactions, and returns
        data used by the reconciliation widget.
        """
        BankStatement = self.env['account.bank.statement']
        BankStatementLine = self.env['account.bank.statement.line']

        # Filter out already imported transactions and create statements
        statement_ids = []
        ignored_statement_lines_import_ids = []
        for st_vals in stmts_vals:
            filtered_st_lines = []
            for line_vals in st_vals['transactions']:
                if not line_vals.get('unique_import_id') or not bool(BankStatementLine.sudo().search([('unique_import_id', '=', line_vals['unique_import_id'])], limit=1)):
                    line_vals['date'] = datetime.datetime.strptime(line_vals['date'], '%d.%m.%Y')
                    line_vals['payment_ref'] = line_vals.pop('name')
                    filtered_st_lines.append(line_vals)
                else:
                    ignored_statement_lines_import_ids.append(line_vals['unique_import_id'])
            if len(filtered_st_lines) > 0:
                # Remove values that won't be used to create records
                st_vals.pop('transactions', None)
                for line_vals in filtered_st_lines:
                    line_vals.pop('account_number', None)
                # Create the satement
                st_vals['line_ids'] = [[0, False, line] for line in filtered_st_lines]
                statement_ids.append(BankStatement.create(st_vals).id)
        if len(statement_ids) == 0:
            pass

        # Prepare import feedback
        notifications = []
        num_ignored = len(ignored_statement_lines_import_ids)
        if num_ignored > 0:
            notifications += [{
                'type': 'warning',
                'message': _(
                    "%d transactions had already been" +
                    "imported and were ignored.") % num_ignored if
                num_ignored > 1 else
                _("1 transaction had already been imported and was ignored."),
                'details': {
                    'name': _('Already imported items'),
                    'model': 'account.bank.statement.line',
                    'ids': BankStatementLine.search(
                        [(
                            'unique_import_id',
                            'in',
                            ignored_statement_lines_import_ids)]).ids
                }
            }]
        return statement_ids, notifications

    def _get_balance_end(self, start_date, end_date):
        headers = {
            'Content-Type': 'application/json; charset=cp1251',
            'token': self.autoclient_token,
            'id': self.autoclient_id,
            'User-Agent': 'клиентское приложение'.encode('utf-8')
        }
        try:
            url = ''
            if self.import_variant == 'today':
                url = f'{self.url_balance}/today?acc={self.bank_acc}'
            elif self.import_variant == 'yesterday':
                url = f'{self.url_balance}/lastday?acc={self.bank_acc}'
            else:
                url = f'{self.url_balance}?acc={self.bank_acc}&startDate={start_date}&endDate={end_date}'

            _logger.info("Request url: {}".format(url))
            response = self.s.get(url, headers=headers, timeout=self.timeout)
        except Exception as error:
            _logger.error("Error in request")
            _logger.error(error)
            return None, None
        if response.status_code == 200:
            # OK
            _logger.info("Response: OK")
            # parse rests
            response_json = response.json()
            try:
                bal_st = response_json['balanceResponse'][0][self.bank_acc[-14:]]['balanceIn']
                bal_end = response_json['balanceResponse'][0][self.bank_acc[-14:]]['balanceOut']
                if bal_st and bal_end:
                    return float(bal_st), float(bal_end)
                else:
                    return None, None
            except Exception:
                return None, None
        elif response.status_code == 400:
            _logger.info("Invalid request")
            raise UserError(_('Invalid request'))
        elif response.status_code == 403:
            _logger.info("Aoutoclient is disabled")
            raise UserError(_('Aoutoclient is disabled'))
        elif response.status_code in [503, 504]:
            _logger.info("Service is temporary unavailable")
            raise UserError(_('Service is temporary unavailable'))
        else:
            _logger.warning('Unable to query xml rests')
            return None, None

    def _import_statement_data(self, statements, start_date, end_date):
        wiz_form_act = {
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'res_model': 'account.p24.sync',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

        st_account = self.bank_acc
        st_data = []

        self.state = 'failure'

        for statement in statements:
            for statement_value in statement.values():
                dt_date = statement_value['BPL_DAT_OD']
                date_str = datetime.datetime.strptime(dt_date, '%d.%m.%Y').strftime('%Y-%m-%d')
                amount = statement_value['BPL_SUM']

                if not any(d.get('date', None) == date_str for d in st_data):
                    # does not exist, create one
                    bal_st, bal_end = self._get_balance_end(
                        datetime.datetime.strptime(dt_date, '%d.%m.%Y').strftime('%d-%m-%Y'),
                        datetime.datetime.strptime(dt_date, '%d.%m.%Y').strftime('%d-%m-%Y')
                    )
                    # name = self.journal_id.sequence_id.with_context(
                    #     ir_sequence_date=date_str).next_by_id()
                    # name = date_str # todo: see later
                    st_data.append({
                        'name': statement_value['BPL_OSND'],
                        'date': datetime.datetime.strptime(dt_date, '%d.%m.%Y'),
                        'balance_start': bal_st,
                        'balance_end_real': bal_end,
                        'transactions': [],
                    })
                for d in st_data:
                    if d['date'] == datetime.datetime.strptime(dt_date, '%d.%m.%Y'):
                        d['transactions'].append({
                            'name': statement_value['BPL_OSND'] + " (" + statement_value['AUT_CNTR_ACC'] + '→' + statement_value[
                                'AUT_MY_ACC'] + ')' + '; Референс проводки: ' + statement_value[
                                        'BPL_REF'] + '; ' + 'Дата валютирования: ' + statement_value[
                                        'BPL_DAT_OD'] + '; ' + 'Время проводки: ' + statement_value[
                                        'BPL_TIM_P'] + '. (ЄДРПОУ: ' + statement_value[
                                        'AUT_CNTR_CRF'] + ';Партнер: ' + statement_value[
                                        'AUT_CNTR_NAM'] + ')',
                            'date': statement_value['BPL_DAT_OD'] if statement_value['TRANTYPE'] == 'C' else statement_value['BPL_DAT_KL'],
                            'amount': amount if statement_value['TRANTYPE'] == 'C' else 0 - float(amount),
                            'unique_import_id': statement_value['BPL_REF'] + '/' + statement_value['ID'] + '/' + statement_value['BPL_DAT_OD'].replace('.', ''),
                            'account_number': self.bank_acc,
                            'partner_name': statement_value['AUT_MY_NAM'] if statement_value['TRANTYPE'] == 'D' else statement_value['AUT_CNTR_NAM'],
                            'ref': statement_value['BPL_REF'],
                            'partner_acc': statement_value['AUT_CNTR_NAM'] if statement_value['TRANTYPE'] == 'C' else statement_value['AUT_MY_ACC'],
                            'partner_edrpou': statement_value['AUT_CNTR_CRF'],
                            # 'pp':row[new_row]['BPL_B_NAM'] if row[new_row]['TRANTYPE'] == 'D' else row[new_row]['BPL_A_NAM']
                        })
        if not st_data:
            _logger.info('received bank statement is empty. do nothing')
            return True

        stmts_vals = self._complete_stmts_vals(st_data, self.journal_id, st_account)
        # Create the bank statements
        statement_ids, notifications = self._create_bank_statements(stmts_vals)

        if not statement_ids:
            return True
        # Now that the import worked out,
        # set it as the bank_statements_source of the journal
        # self.journal_id.bank_statements_source = 'p24_import' # todo: check later
        # Finally dispatch to reconciliation interface
        action = self.env.ref('account.action_bank_statement_tree').read()[0]
        action.update({
            'domain': [('journal_id', '=', self.journal_id.id)]
        })
        return action

    def _get_statement_stdate(self):
        # today in datetime
        today = fields.Date.from_string(fields.Date.today())
        # default is beggining of the year
        stdate = today.strftime('01.01.%Y')
        domain = [
            '&',
            ('journal_id', '=', self.journal_id.id),
            ('date', '<=', fields.Date.today())]
        stmts = self.env['account.bank.statement'].search(domain)
        if stmts:
            # find latest statement and check if it not in future
            # return last statement date or today
            stmts = stmts.sorted(key=lambda r: r.date, reverse=True)
            last_stmt = stmts[0]
            last_stmt_date = fields.Date.from_string(last_stmt.date)
            return last_stmt_date.strftime('%d.%m.%Y')
        else:
            # if nothing found
            return stdate

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
            "recipient_nceo": self.partner_id.company_registry,
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

    def _do_statement_import(self):
        wiz_form_act = {
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'res_model': 'account.p24.sync',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
        start_date = False
        end_date = False
        if self.import_variant == 'today':
            url = self.url_transactions + "/today?acc=%s" % self.bank_acc
        elif self.import_variant == 'yesterday':
            url = self.url_transactions + "/lastday?acc=%s" % self.bank_acc
        else:
            if not self.start_import_date:
                self.state = 'failure'
                raise UserError(_('Empty start date'))
            if (not self.start_import_date and not self.end_import_date) or (
                    self.start_import_date > self.end_import_date):
                self.state = 'failure'
                raise UserError(_('Empty dates or start date is bigger than end date'))
            start_date = self.start_import_date.strftime('%d-%m-%Y')
            end_date = self.end_import_date.strftime('%d-%m-%Y')
            url = self.url_transactions + "?acc=%s&startDate=%s&endDate=%s" % (self.bank_acc, start_date, end_date)

        headers = {
            'Content-Type': 'application/json; charset=cp1251',
            'token': self.autoclient_token,
            'id': self.autoclient_id,
            'User-Agent': 'клиентское приложение'.encode('utf-8')
        }

        _logger.info("Request url: {}".format(url))
        try:
            response = self.s.get(url, headers=headers, timeout=self.timeout)
        except Exception:
            _logger.info("Error in request")
            raise UserError(_('Error in request'))

        if response.status_code == 200:
            # OK
            _logger.info("Response: OK")
            resp_json = response.json()
            self.task = 'nothing'
            # parse statement
            res = self._import_statement_data(resp_json['StatementsResponse']['statements'], start_date, end_date)
            return res
        elif response.status_code == 401:
            self.state = 'loginpasswd'
            return wiz_form_act
        elif response.status_code == 400:
            _logger.info("Invalid request")
            raise UserError(_('Invalid request'))
        elif response.status_code == 403:
            _logger.info("Aoutoclient is disabled")
            raise UserError(_('Aoutoclient is disabled'))
        elif response.status_code in [503, 504]:
            _logger.info("Service is temporary unavailable")
            raise UserError(_('Service is temporary unavailable'))

    def _do_task(self):
        '''Do business task after session was built.'''
        wiz_form_act = {
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'res_model': 'account.p24.sync',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
        if self.task == 'nothing':
            self.state = 'success'
            return wiz_form_act

        if self.task == 'statement_import':
            self.state = 'date_choose'
            return wiz_form_act
            # return self._do_statement_import()

        if self.task == 'send_payment':
            return self._do_send_payment()

    def do_sync(self):
        '''Public function to sync data with Privat24.'''
        self.ensure_one()
        wiz_form_act = {
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'res_model': 'account.p24.sync',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

        if self.state == 'choose_acc':
            return wiz_form_act

        if not self.autoclient_id or not self.autoclient_token:
            self.state = 'loginpasswd'
            return wiz_form_act
        else:
            return self._do_task()

    def do_import(self):
        return self._do_statement_import()

    def do_sync_next(self):
        if not self.recip_bank.acc_number or not self.recip_bank.bank_name or not self.recip_bank.bank_bic or not self.recip_bank.bank_id.company_registry:
            raise UserError(_('Provide partner bank info!'))
        self.state = 'success'
        return self._do_sync()
