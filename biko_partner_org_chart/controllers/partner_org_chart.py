# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request


class PartnerOrgChartController(http.Controller):
    _parents_level = 5  # FP request

    def _check_partner(self, partner_id, **kw):
        if not partner_id:
            return None
        partner_id = int(partner_id)

        if 'allowed_company_ids' in request.env.context:
            cids = request.env.context['allowed_company_ids']
        else:
            cids = [request.env.company.id]

        Partner = request.env['res.partner'].with_context(allowed_company_ids=cids)
        # check and raise
        if not Partner.check_access_rights('read', raise_exception=False):
            return None
        try:
            Partner.browse(partner_id).check_access_rule('read')
        except AccessError:
            return None
        else:
            return Partner.browse(partner_id)

    def _prepare_partner_data(self, partner):
        return dict(
            id=partner.id,
            name=partner.name,
            link='/mail/view?model=%s&res_id=%s' % ('res.partner', partner.id,),
            manager_id=partner.id,
            manager_name=partner.name,
            direct_sub_count=len(partner.child_ids),
            indirect_sub_count=partner.child_all_count,
            phone=partner.phone,
            phone_link = f'tel:{partner.phone}',
            mobile=partner.mobile,
            mobile_link = f'tel:{partner.mobile}',
            function = partner.function or '',
        )

    @http.route('/partner/biko_get_org_chart', type='json', auth='user')
    def get_org_chart(self, partner_id, **kw):
        partner = self._check_partner(partner_id, **kw)
        if not partner:  # to check
            return {
                'parents': [],
                'children': [],
            }

        # compute partner data for org chart
        ancestors, current = request.env['res.partner'].sudo(), partner.sudo()
        while current.parent_id and len(ancestors) < self._parents_level + 1:
            ancestors += current.parent_id
            current = current.parent_id

        values = dict(
            self=self._prepare_partner_data(partner),
            parents=[
                self._prepare_partner_data(ancestor)
                for idx, ancestor in enumerate(ancestors)
                if idx < self._parents_level
            ],
            parents_more=len(ancestors) > self._parents_level,
            children=[self._prepare_partner_data(child) for child in partner.child_ids],
        )
        values['parents'].reverse()
        return values

    @http.route('/partner/biko_get_subordinates', type='json', auth='user')
    def get_subordinates(self, partner_id, subordinates_type=None, **kw):
        """
        Get partner subordinates.
        Possible values for 'subordinates_type':
            - 'indirect'
            - 'direct'
        """
        partner = self._check_partner(partner_id, **kw)
        if not partner:  # to check
            return {}

        if subordinates_type == 'direct':
            res = partner.child_ids.ids
        elif subordinates_type == 'indirect':
            res = (partner.subordinate_ids - partner.child_ids).ids
        else:
            res = partner.subordinate_ids.ids
        return res
