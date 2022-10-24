import logging
from odoo import models

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError as err:
    _logger.debug(err)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

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