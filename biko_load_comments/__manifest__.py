# -*- coding: utf-8 -*-
{
    'name': "BIKO: Import comments to opportunities",
    'version': '14.0.1.1.1',
    'author': 'Borovlev AS',
    'company': 'BIKO',
    "depends": ['crm'],
    "data": [
        'views/assets.xml',
        'wizard/biko_import_recs_views.xml',
        'security/ir.model.access.csv',
    ],
    "qweb": [
        'views/biko_import_comments.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    "sequence": -1,
}
