from odoo import fields, models

class JiraSettings(models.Model):
    _name = "jira.settings"

    url = fields.Char(string = "URL", required = True)
    login = fields.Char(string = "User name")
    password = fields.Char(string = "Password")
    