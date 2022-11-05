from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    jira_login = fields.Char(
        string='JIRA Login',
        config_parameter='biko_jira_integration.jira_login'
    )

    jira_password = fields.Char(
        string='JIRA Password',
        config_parameter='biko_jira_integration.jira_password'
    )
