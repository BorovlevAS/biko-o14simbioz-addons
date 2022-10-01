# -*- coding: utf-8 -*-
{
    'name': "BIKO: add hierarchy tree to project list and task list",
    'description': """Добавляет видимость иерархии проектов и задач в соответствующие списки""",
    'version': '14.0.1.1.0',
    'author': 'Borovlev AS',
    'company': 'BIKO',
    "depends": ['project', 'project_org_chart'],
    "data": [
        'views/project_task_views.xml',
        'views/project_project_views.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False
}
