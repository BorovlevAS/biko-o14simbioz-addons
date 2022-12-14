# -*- coding: utf-8 -*-
{
    'name': "BIKO: Печатная форма счета",
    'version': '14.0.1.1.2',
    'author': 'Borovlev A.S.',
    'company': 'Quick Decisions',
    "depends": ['sale', 'biko_stamp_signature', 'kw_account_partner_requisites', 'biko_kw_so_doc_base_patch'],
    "data": [
        'reports/rahunok_template.xml',
        'views/actions.xml'
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}