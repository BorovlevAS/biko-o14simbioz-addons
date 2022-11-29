import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    legal_address = fields.Many2one(comodel_name='res.partner')