from odoo import fields, models

class JiraProjectCategories(models.Model):
    _name = "jira.project.categories"

    url = fields.Char(string="URL")
    jira_id = fields.Char(string="ID")
    name = fields.Char(string="Name")
    jira_description = fields.Char(string="Description")
    load_projects = fields.Boolean(string="Load projects with this category")
    