{
    'name': 'MonoBank',

    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',

    'category': 'Accounting',
    'license': 'OPL-1',
    'version': '15.0.1.0.3',

    'depends': ['kw_bank_import_base', ],

    'installable': True,

    'data': [
        'views/mono_personal_info.xml',
        'security/ir.model.access.csv',
    ],

    'images': [
        'static/description/icon.png',
    ],

    'price': 10,
    'currency': 'EUR',
}
