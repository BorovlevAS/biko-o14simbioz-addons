from odoo import http, models, fields, _, SUPERUSER_ID
from odoo.http import request, JsonRequest
import json

import logging

_logger = logging.getLogger(__name__)

class BIKONextelController(http.Controller):

    @http.route('/nextel/call/new', type='json', auth='none', methods=['GET', 'POST'], csrf=False)
    def nextel_new_call(self):
        _logger.info('\n\n\n*************   nextel_new_call  START **********************\n')
        data = request.jsonrequest
        call_data = data['call']
        _logger.info('data: %s', json.dumps(data, indent=4, sort_keys=True))

        new_call_vals = {
            'name': 'Call from number {}'.format(call_data['from']),
            'call_id': call_data['id'],
            'from_call': call_data['from'],
            'partner_phone': call_data['from'],
            'partner_mobile': call_data['from'],
            'date': call_data['date'],
            'direction': 'in' if call_data['direction'] == 'IN' else 'out',
            'nextel_direction': call_data['direction'],
            'nextel_source': call_data['source'],
            'call_event': data['event'],
        }
        phonecall_env = request.env['crm.phonecall'].sudo()
        phone_formatted = phonecall_env.phone_format(call_data['from'])
        domain = [
            '|',
            '|',
            '|',
            ('biko_mobile_e164', '=', phone_formatted),
            ('biko_phone_e164', '=', phone_formatted),
            ('mobile', '=', phone_formatted),
            ('phone', '=', phone_formatted),
        ]
        _logger.info('ResPartner search domain: %s', domain)

        from_call_partner = request.env['res.partner'].sudo().search(domain, limit=1)
        if from_call_partner:
            new_call_vals['partner_id'] = from_call_partner.id
            if from_call_partner.email:
                new_call_vals['email_from'] = from_call_partner.email

        phonecall = phonecall_env.create(new_call_vals)
        _logger.info('Phonecall created: %s', phonecall)

        _logger.info('\n\n\n*************   nextel_new_call  END **********************\n')
        return json.dumps({'status': 'success', 'phonecall_id': phonecall.id})