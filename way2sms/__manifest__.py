{
    'name': "Way2SMS",
    'summary': """ This App has the ability to send SMS using Way2sms """,
    'version': '10.0.1.0.0',
    'category': 'SMS app',
    'website': "viki2.odoo.com",
    'author': "Vignesh",
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'images': ['images/main_screenshot.png'],
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/way2sms_view.xml',
        'views/way2sms_base_view.xml',
    ],
}
