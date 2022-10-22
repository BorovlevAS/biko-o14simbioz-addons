# -*- coding: utf-8 -*-
{
    'name': "BIKO: патч модуля телефонии",
    'version': '14.0.1.1.1',
    'author': 'Borovlev A.S.',
    'company': 'BIKO Solutions',
    "depends": ['phone_validation_extra', 'nextel', 'crm_phonecall'],
    "data": [
        'views/assets.xml',
        'views/res_partner_views.xml',
        'views/crm_phonecall.xml'
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}