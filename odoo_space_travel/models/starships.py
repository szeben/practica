from odoo import models, fields, api

class Starships(models.Model):
    
    _name = 'space.starship'
    _description = 'Starship Info'
    
    name = fields.Char(string = 'Name', required=True)
    job = fields.Char(string = 'Job', required=True)
    
    level = fields.Char(string = 'Level', required=True)