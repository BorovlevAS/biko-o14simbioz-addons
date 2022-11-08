{
    'name': 'Bank statement import base',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Accounting',
    'license': 'OPL-1',
    'version': '15.0.1.0.9',

    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_view.xml',
        'views/account_bank_statement_view.xml',
        'views/res_bank_view.xml',
        'wizard/journal_creation.xml',
    ],

    'images': [
        'static/description/cover.png',
        'static/description/icon.png',
    ],

    'price': 10,
    'currency': 'EUR',
}
