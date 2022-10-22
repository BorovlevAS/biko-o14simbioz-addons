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
        
        client_phone = call_data['to'][0] if len(call_data['to']) > 0 else ''

        phonecall_env = request.env['crm.phonecall'].sudo()

        if new_call_vals['direction'] == 'in':
            phone_formatted = phonecall_env.phone_format(call_data['from'])
            # op_num = call_data['to'][0] if len(call_data['to']) > 0 else ''
        else:
            phone_formatted = phonecall_env.phone_format(client_phone)
            new_call_vals['partner_phone'] = client_phone
            new_call_vals['partner_mobile'] = client_phone
            # op_num = call_data['from']

        # TODO: need to add user for phonecall
        # find user by Operator ID in nextel operators
        # op_id = request.env['nextel.operator'].sudo().search([('nextel_employee_number', '=', op_num)], limit=1)
        # user_id = op_id.user_id.id if op_id else None
        # new_call_vals['user_id'] = user_id
        
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

    @http.route('/nextel/call/answer', type='json', auth='none', methods=['GET', 'POST'], csrf=False)
    def nextel_call_answer(self):
        _logger.info('\n\n\n*************   nextel_call_answer  START **********************\n')
        data = request.jsonrequest
        call_data = data['call']
        _logger.info('data: %s', json.dumps(data, indent=4, sort_keys=True))

        # update crm.phonecall by call_id
        phonecall = request.env['crm.phonecall'].sudo().search([('call_id', '=', call_data['id'])], limit=1)
        phonecall.update({
            'nextel_state': call_data['state'],
            'call_event': data['event'],
        })

        # notify operator
        if call_data['direction'].upper() == 'IN':
            nextel_operator_domain = [
                ('nextel_employee_number', 'in', call_data['to']),
                ('user_id', '!=', False)
            ]
        else:
            nextel_operator_domain = [
                ('nextel_employee_number', '=', call_data['from']),
                ('user_id', '!=', False)
            ]
        
        _logger.info('NextelOperator search nextel_operator_domain: %s', nextel_operator_domain)
        notify_operators = request.env['nextel.operator'].sudo().search(nextel_operator_domain)
        if notify_operators:
            for operator in notify_operators:
                bus_message = {
                    'call_event': phonecall.call_event,
                }
                notifications = [(operator.user_id.channel_phonecall_update, bus_message)]
                _logger.info('Sent notify: %s', notifications)
                request.env['bus.bus'].sendmany(notifications)

        _logger.info('\n\n\n*************   nextel_call_answer  END **********************\n')
        return json.dumps({'status': 'success'})
