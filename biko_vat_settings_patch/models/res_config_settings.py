from odoo import api, fields, models, _
from odoo.addons.account_tax_invoice.models.res_config_settings import ResConfigSettings


class BIKOResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    uavat_account_id = fields.Many2one(
        "account.account",
        "VAT account",
        related="company_id.uavat_account_id",
        readonly=False,
    )

    uavat_unconf_tax_liab_account_id = fields.Many2one(
        "account.account",
        "Unconfirmed tax liability account",
        related="company_id.uavat_unconf_tax_liab_account_id",
        readonly=False,
    )

    uavat_conf_tax_liab_account_id = fields.Many2one(
        "account.account",
        "Confirmed tax liabilities account",
        related="company_id.uavat_conf_tax_liab_account_id",
        readonly=False,
    )

    uavat_unconf_tax_credit_account_id = fields.Many2one(
        "account.account",
        "Unconfirmed tax credit account",
        related="company_id.uavat_unconf_tax_credit_account_id",
        readonly=False,
    )

    uavat_conf_tax_credit_account_id = fields.Many2one(
        "account.account",
        "Confirmed tax credit account",
        related="company_id.uavat_conf_tax_credit_account_id",
        readonly=False,
    )

    uavat_journal_id = fields.Many2one(
        "account.journal",
        "VAT journal",
        related="company_id.uavat_journal_id",
        readonly=False,
    )

    uavat_tax_id = fields.Many2one(
        "account.tax", "VAT Rate", related="company_id.uavat_tax_id", readonly=False
    )

    uavat_account_analytic_settlements = fields.Boolean(
        related="company_id.uavat_account_analytic_settlements",
        string="Contract settlements",
        readonly=False,
    )

    uavat_ati_product_id = fields.Many2one(
        "product.product",
        "Account tax invoice product",
        domain=[("ati_product", "=", True)],
        related="company_id.uavat_ati_product_id",
        readonly=False,
    )


ResConfigSettings.uavat_account_id = BIKOResConfigSettings.uavat_account_id
ResConfigSettings.uavat_unconf_tax_liab_account_id = (
    BIKOResConfigSettings.uavat_unconf_tax_liab_account_id
)
ResConfigSettings.uavat_conf_tax_liab_account_id = (
    BIKOResConfigSettings.uavat_conf_tax_liab_account_id
)
ResConfigSettings.uavat_unconf_tax_credit_account_id = (
    BIKOResConfigSettings.uavat_unconf_tax_credit_account_id
)
ResConfigSettings.uavat_conf_tax_credit_account_id = (
    BIKOResConfigSettings.uavat_conf_tax_credit_account_id
)
ResConfigSettings.uavat_journal_id = BIKOResConfigSettings.uavat_journal_id
ResConfigSettings.uavat_tax_id = BIKOResConfigSettings.uavat_tax_id
ResConfigSettings.uavat_account_analytic_settlements = (
    BIKOResConfigSettings.uavat_account_analytic_settlements
)
ResConfigSettings.uavat_ati_product_id = BIKOResConfigSettings.uavat_ati_product_id
