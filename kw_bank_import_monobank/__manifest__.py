{
    'name': 'Import Monobank statement',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Accounting',
    'license': 'OPL-1',
    'version': '15.0.1.0.6',

    'depends': ['kw_bank_import_base', 'kw_mono_bank_personal',
                'kw_currency_monobank'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/account_view.xml',
    ],

    'images': [
        'static/description/cover.png',
        'static/description/icon.png',
    ],

    'price': 100,
    'currency': 'EUR',
}
