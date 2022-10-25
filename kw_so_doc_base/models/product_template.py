from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    kw_is_added_to_so = fields.Boolean(
        string="Include in reports printed from SO", default=True,
        help="If checked, the product will be added to the SO.")
