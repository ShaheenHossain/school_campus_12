# -*- coding: utf-8 -*-

from odoo import models, fields, api


import datetime
from datetime import datetime
from odoo.exceptions import UserError
import re

from odoo import fields, api,models,_






class sample(models.Model):
	_name = "hr.helpdesk"


	name=fields.Char(string="Student NameS")
	contact =fields.Char(string="Contact")
	email = fields.Char(string="Email")
	state = fields.Selection([('draft','Draft'),
								('hr','HR'),
								('it','IT'),
								('gravience','Gravience'),
								('done','Done')],default="draft")
 	



 	@api.multi
 	def approval1(self):
 			self.write({'state':'hr'})
 	@api.multi
 	def approval2(self):
 			self.write({'state':'it'})
 	@api.multi
 	def approval3(self):
 			self.write({'state':'gravience'})
	