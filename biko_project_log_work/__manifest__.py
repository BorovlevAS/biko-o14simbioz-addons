# -*- coding: utf-8 -*-
{
    'name': "BIKO: Протоколирование работы в проекте",
    'version': '14.0.1.1.0',
    'author': 'Borovlev A.S.',
    'company': 'Quick Decisions',
    "depends": ['project', 'hr_timesheet'],
    "data": [
        'wizards/project_log_work_views.xml',
        'views/project_task_views.xml',
        'security/ir.model.access.csv',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}