# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Org Chart',
    'summary': 'Partner Org Chart',
    'author': 'Simbioz, Sasha Kochyn',
    'maintainer': 'Simbioz Holding LLC',
    'website': 'https://simbioz.ua',
    'category': 'Sales/CRM',
    'version': '14.0.1.0.3',
    'depends': [
        'contacts', 'biko_nextel_patch'
    ],
    'data': [
        'views/assets.xml',
        'views/partner.xml'
    ],
    'qweb': [
        'static/src/xml/partner_org_chart.xml',
    ],
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
