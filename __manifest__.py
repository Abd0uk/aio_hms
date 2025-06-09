# type: ignore
# noqa

{
    'name': 'AIO Hospital Management System',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'description': 'Complete Hospital Management System for managing patients',
    'author': 'Your Name',
    'website': 'http://www.yourwebsite.com',
    'category': 'Healthcare',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_view.xml',
        'views/menus.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': 'aio_hms/static/description/icon.png',
}