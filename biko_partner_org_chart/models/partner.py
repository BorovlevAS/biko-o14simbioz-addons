# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = "res.partner"
    _parent_name = "parent_id"
    _parent_store = True

    subordinate_ids = fields.One2many(
        comodel_name='res.partner',
        string='Subordinates',
        compute='_compute_subordinates',
        help="Direct and indirect subordinates",
        store=False,
        compute_sudo=True)
    child_all_count = fields.Integer(
        string='Indirect Subordinates Count',
        compute='_compute_subordinates',
        store=True,
        compute_sudo=True)
    parent_path = fields.Char(
        index=True)

    def _get_subordinates(self, parents=None):
        """
        Helper function to compute subordinates_ids.
        Get all subordinates (direct and indirect) of an partner.
        """
        if not parents:
            parents = self.env[self._name]

        indirect_subordinates = self.env[self._name]
        parents |= self
        direct_subordinates = self.child_ids - parents
        for child in direct_subordinates:
            child_subordinate = child._get_subordinates(parents=parents)
            indirect_subordinates |= child_subordinate
        return indirect_subordinates | direct_subordinates

    @api.depends('child_ids', 'child_ids.child_all_count')
    def _compute_subordinates(self):
        for partner in self:
            partner.subordinate_ids = partner._get_subordinates()
            partner.child_all_count = len(partner.subordinate_ids)

    def add_new_child_contact(self):
        action = self.env.ref('biko_partner_org_chart.biko_res_partner_child_action').read()[0]
        action['views'] = [(self.env.ref('biko_partner_org_chart.biko_view_res_partner_child_form').id, 'form')]
        action['context'] = {
            'default_parent_id': self.id,
            'default_street': self.street,
            'default_street2': self.street2,
            'default_city': self.city,
            'default_state_id': self.state_id.id,
            'default_zip': self.zip,
            'default_country_id': self.country_id.id,
            'default_lang': self.lang,
            'default_user_id': self.user_id.id,
            'default_type': 'other',
        }
        return action
