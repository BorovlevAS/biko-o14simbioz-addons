# -*- coding: utf-8 -*-
{
    'name': "BIKO: Патч печатной формы KW_SO_RAHF",
    'version': '14.0.1.1.1',
    'author': 'Borovlev A.S.',
    'company': 'Quick Decisions',
    "depends": ['sale', 'biko_stamp_signature'],
    "data": [
        'reports/rahunok_template.xml',
        'views/actions.xml'
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}