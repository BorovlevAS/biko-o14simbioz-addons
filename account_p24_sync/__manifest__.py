# -*- coding: utf-8 -*-
{
    'name': 'PrivatBank online synchronization',
    'author': 'Simbioz, Sasha Kochyn',
    'website': 'https://simbioz.ua',
    'summary': "Sync statements with PrivatBank online",
    'category': 'Invoices & Payments',
    'version': '14.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/p24_sync_wizard_view.xml',
        'views/account_journal_view.xml',
        'views/account_payment_view.xml',
        'views/res_partner_bank.xml',
        'views/partner.xml',
        'data/account_payment_method.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
