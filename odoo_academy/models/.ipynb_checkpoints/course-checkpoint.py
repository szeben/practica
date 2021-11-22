#-*- coding: utf-8 -*-

from odoo import models, fields, api

class Course (models.Model):
    _name='academy.course'
    _description='course info'
    
    name=fields.Char(string='title', required=True)
    description=fields.Text(string='Description')
    level=fields.Char(string='level')
    #level=fields.Selection(string='level',
    #                      selection=[('beginner','Beginner'), ('intermediate','Intermediate'),('advanced','Advanced')],
    #                      copy=False)
    active=fields.Boolean(string='Active',default=True)
    
    session_ids=fields.One2many(comodel_name='academy.session',
                               inverse_name='course_id',
                               string='Sessions')
    
    base_price=fields.Float(string=' Base Price',default=0.00)
    
    additional_fee=fields.Float(string='Additional Fee', default=10.00)
    
    total_price=fields.Float(string='Total price',readonly=True)
    
    @api.onchange('base_price', 'additional_fee')
    def _onchange_total_price(self):
        if self.base_price <0.0:
            raise UserError('Base price cannot be set as negative.')
        
        self.total_price=self.base_price+self.additional_fee
    
                        