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
    
                        