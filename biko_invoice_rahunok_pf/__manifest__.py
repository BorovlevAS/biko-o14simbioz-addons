# -*- coding: utf-8 -*-
{
    'name': "BIKO: Печатная форма Счет для документа Invoice",
    'version': '14.0.1.1.0',
    'author': 'Borovlev A.S.',
    'company': 'BIKO Solutions',
    "depends": ['account', 'biko_stamp_signature', 'kw_account_partner_requisites'],
    "data": [
        'views/account_move_views.xml',
        'reports/rahunok_template.xml',
        'views/actions.xml'
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}