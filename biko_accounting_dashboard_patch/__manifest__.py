# -*- coding: utf-8 -*-
{
    'name': "BIKO: Патч модуля base accounting kit",
    'version': '14.0.1.1.0',
    'author': 'Borovlev A.S.',
    'company': 'BIKO Solutions',
    "depends": ['base_accounting_kit'],
    "data": [
        'views/assets.xml',
        'views/actions.xml',
        # 'views/template_patch.xml'
    ],

    "qweb": ["static/src/xml/template_patch.xml"],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
