# *-* coding : utf-8 -*-

from odoo import models, fields, api

class Workers(models.Model):
    
    _name = 'space.workers'
    _description = 'Workers Info'
    
    name = fields.Char(string = 'Name', required=True)
    job = fields.Char(string = 'Job', required=True)
    
    level = fields.Char(string = 'Level', required=True)
    