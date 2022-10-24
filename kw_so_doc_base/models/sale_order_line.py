import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'sale.order.line'

    kw_is_added_to_so = fields.Boolean(
        string='Is a configurable product',
        compute='_compute_kw_is_added_to_so', )

    def _compute_kw_is_added_to_so(self):
        for obj in self:
            obj.kw_is_added_to_so = \
                obj.product_id.product_tmpl_id.kw_is_added_to_so
