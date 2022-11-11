import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError as err:
    _logger.debug(err)

class AccountMove(models.Model):
    _inherit = 'account.move'

    kw_amount_ukr_text = fields.Char(compute = '_compute_kw_amount_ukr_text')
    kw_taxed_ukr_text = fields.Char(compute = '_compute_kw_taxed_ukr_text')
    company_partner_id = fields.Many2one(related='company_id.partner_id', string = 'Our Partner')
    kw_amount_untaxed_ukr_text = fields.Char(compute = '_compute_kw_amount_untaxed_ukr_text')
    amount_residual_ukr_text = fields.Char(compute = '_compute_amount_residual_ukr_text')

    @api.onchange('company_id')
    def _biko_onchange_company_id(self):
        for order in self:
            res = self.env['res.partner.bank'].sudo().search([
                            ('partner_id', '=', order.company_id.partner_id.id)
                            ])
            available_bank_ids = res._origin
            order.bank_id = available_bank_ids[:1]._origin

    bank_id = fields.Many2one('res.partner.bank', string = "Bank Account",
            domain = "[('partner_id', '=', company_partner_id)]",
            default = _biko_onchange_company_id,
            tracking = True)

    def _compute_amount_residual_ukr_text(self):
        for obj in self:
            obj.amount_residual_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.amount_residual), lang='uk'),
                obj.currency_id.biko_get_currency_name(obj.amount_residual, False),
                round(100 * (obj.amount_residual - int(obj.amount_residual))),
                obj.currency_id.biko_get_currency_name(round(100 * (obj.amount_residual - int(obj.amount_residual))), True),
            ).capitalize()

    def _compute_kw_amount_ukr_text(self):
        for obj in self:
            obj.kw_amount_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.amount_total), lang='uk'),
                obj.currency_id.biko_get_currency_name(obj.amount_tax, False),
                round(100 * (obj.amount_total - int(obj.amount_total))),
                obj.currency_id.biko_get_currency_name(round(100 * (obj.amount_total - int(obj.amount_total))), True),
            ).capitalize()

    def _compute_kw_taxed_ukr_text(self):
        for obj in self:
            obj.kw_taxed_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.amount_tax), lang='uk'),
                obj.currency_id.biko_get_currency_name(obj.amount_tax, False),
                round(100 * (obj.amount_tax - int(obj.amount_tax))),
                obj.currency_id.biko_get_currency_name(round(100 * (obj.amount_tax - int(obj.amount_tax))), True),
            ).capitalize()

    def _compute_kw_amount_untaxed_ukr_text(self):
        for obj in self:
            obj.kw_amount_untaxed_ukr_text = '{} {} {:0>2} {}'.format(
                num2words(int(obj.amount_untaxed), lang='uk'),
                obj.currency_id.biko_get_currency_name(obj.amount_tax, False),
                round(100 * (obj.amount_untaxed - int(obj.amount_untaxed))),
                obj.currency_id.biko_get_currency_name(round(100 * (obj.amount_untaxed - int(obj.amount_untaxed))), True),
            ).capitalize()

    def biko_get_invoice_filename(self):
        doc_num = self.name
        doc_date = self.invoice_date.strftime("%d.%m.%Y")
        return f'Рахунок № {doc_num} від {doc_date}'