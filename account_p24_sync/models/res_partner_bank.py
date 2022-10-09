# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    is_card = fields.Boolean(
        string='Is card',
        default=False,
    )
