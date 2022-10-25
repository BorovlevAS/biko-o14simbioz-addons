{
    'name': 'SO print document for Ukraine',

    'version': '14.0.1.0.2',
    'author': 'Kitworks Systems',
    'website': 'https://kitworks.systems/',
    'license': 'OPL-1',
    'category': 'Accounting',

    'depends': ['sale', 'kw_account_partner_requisites', ],

    'data': [
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,

    'images': [
        'static/description/cover.png',
        'static/description/icon.png',
    ],

}
