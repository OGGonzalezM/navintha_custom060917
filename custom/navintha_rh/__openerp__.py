# -*- coding: utf-8 -*-
{
    'name': "Navintha - RH",

    'summary': """
        Campos agregados para Navintha""",

    'description': """
       Creacion de los campos requeridos para navintha
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr','kpi'],

    # always loaded
    'data': [
        'views/navintha_hr_view.xml',
    ],
    'installable':True,
    'auto_install':False,
}
