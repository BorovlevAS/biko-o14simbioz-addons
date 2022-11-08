{
    'name': 'monobank currency rates',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Customizations',
    'license': 'OPL-1',
    'version': '15.0.1.0.3',

    'depends': ['kw_currency_base', 'kw_mono_bank_personal',
                'kw_currency_code'],

    'images': [
        'static/description/cover.png',
        'static/description/icon.png',
    ],

    'data': [
        'security/ir.model.access.csv',
    ],
    'price': 30,
    'currency': 'EUR',

    'live_test_url': 'https://kw-currency-monobank.demo13.kitworks.systems',
}
