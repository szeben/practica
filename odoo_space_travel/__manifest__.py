# -*- coding: utf-8 -*-

{
    'name' : 'Odoo Space Travel',
    
    'summary' : """App to manage space travel""",
    
    'description' : """
    App to manage:
    - Starship properties
    - Workers
    - Travel summary
    """,
    
    'author' : 'Julio Jaeger',
    
    'website' : 'https://technestudioit.com',
    
    'category' : 'Travel',
    'version' : '0.1',
    
    'depends' : ['base'],
    
    'data' : [
        'security/space_travel_security.xml',
        'security/ir.model.access.csv',
        'views/space_travel_menuitems.xml',
        'views/worker_views.xml'
    ],
    
    'demo' : [
        'demo/space_travel_demo.xml',
    ],
}