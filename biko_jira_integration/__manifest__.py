# -*- coding: utf-8 -*-
{
    'name': "BIKO: Интеграция с JIRA",
    'version': '14.0.1.1.0',
    'author': 'Borovlev A.S.',
    'company': 'BIKO SOLUTIONS',
    'category': 'BIKO Apps/JIRA Integration',
    "depends": ['base', 'project', 'biko_project_key_ux'],
    "data": [
        # security
        'security/jira_groups.xml',
        'security/ir.model.access.csv',
        
        'views/res_config_settings_views.xml',
        'views/jira_project_category_views.xml',
        'views/jira_menus.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}