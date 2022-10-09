from odoo import fields, models, api


class Partner(models.Model):
    _inherit = 'res.partner'

    company_registry = fields.Char(
        string='Reg. ID',
        index=True,
    )

    _sql_constraints = [
        ('company_registry_uniq', 'unique(company_registry, company_id)', 'The Reg. ID must be unique per company!'),
    ]
