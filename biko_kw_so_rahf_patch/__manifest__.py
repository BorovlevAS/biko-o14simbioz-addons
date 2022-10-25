# -*- coding: utf-8 -*-
{
    'name': "BIKO: Патч печатной формы KW_SO_RAHF",
    'version': '14.0.1.1.1',
    'author': 'Borovlev A.S.',
    'company': 'Quick Decisions',
    "depends": ['kw_so_rahf', 'biko_stamp_signature'],
    "data": [
        'reports/templates.xml',
        'views/actions.xml'
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}