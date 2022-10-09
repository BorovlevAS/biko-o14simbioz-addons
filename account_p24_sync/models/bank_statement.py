# -*- coding: utf-8 -*-

from odoo import fields, models


class BankStatement(models.Model):
    _inherit = "account.bank.statement.line"

    sender_account = fields.Char(
        string="Sender's account",
    )
    beneficiary_account = fields.Char(
        string="Beneficiary's account"
    )
    unique_import_id = fields.Char(
        string='Unique import id',
    )
    bank_account_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank account',
    )
