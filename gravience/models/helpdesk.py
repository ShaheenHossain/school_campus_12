# -*- coding: utf-8 -*-

from odoo import models, fields, api


import datetime
from datetime import datetime
from odoo.exceptions import UserError
import re

from odoo import fields, api,models,_








class help_desk_hr_view(models.Model):
	_name = 'hr.helpdesk'
	_inherit = 'ir.needaction_mixin'

	
	name = fields.Many2one('hr.employee',required=True)
	reason = fields.Char('Issue of subject',required=True)
	description = fields.Text('Description',required=True)
	attach = fields.Binary(string="Attachment")
	mobile=fields.Char(string='Mobile')
	email=fields.Char(string='Email')
	designation=fields.Char('Designation')
	sending_date=fields.Datetime(string="Complaint Date",readonly=True)
	# department_help_desk=fields.Many2one('hr.help_department',string='Please Select issue of Department')
	status = fields.Selection([('draft','Draft'),
								('hr','HR'),
								('it','IT'),
								('gravience','Gravience'),
								('done','Done')],default="draft")
	replay_message = fields.Text(string="Manager- Remarks")
	
	priority=fields.Selection([('urgent','Urgent'),('high','High'),('Medium','medium'),('normal','Normal')])
	# high=fields.Boolean(string="High")
	# medium=fields.Boolean('Medium')
	# normal=fields.Boolean('Normal')
	# doit=fields.Boolean('Do It')

	department_help_desk = fields.Selection([('hr','HR'),
											('it','IT'),
											('gravience','Gravience')], string="Please Select Issue of Department")



	@api.constrains('name')
	@api.onchange('name')
	def getting_today_dattime(self):
		data=datetime.now()
		self.sending_date=data


	@api.multi
	def approval(self):

		if self.department_help_desk == "hr":
			self.write({'status':"hr"})
		if self.department_help_desk == "it":
			self.write({'status':"it"})
		if self.department_help_desk == "gravience":
			self.write({'status':"gravience"})

	@api.multi
	def replayer_action(self):
		if self.replay_message==False:
			raise UserError("Please write message in replay message")
		else:
			template = self.env.ref('bi_hr.help_desk_mail')
			self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
			self.write({'status':'replied'})


		self.write({'status':"done"})

	

	# @api.multi
	# def Reply_help_desk(self):
	# 	if self.replay_message==False:
	# 		raise UserError("Please write message in replay message")
	# 	else:
	# 		template = self.env.ref('bi_hr.help_desk_mail')
	# 		self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
	# 		self.write({'status':'replied'})
	


	
	@api.model
	def _needaction_domain_get(self):
		return [('status','in',('draft','hr','it','done'))]

		# employees = self.env['hr.employee'].search([])
		# for employee in employees:
		# 	print employee.name,"333333333333333333333333333333333333333"
		# 	print self.env.user.name,"22222222222222222222222222222222222222"
		# 	if self.env.user.name == employee.name:
		# 		if employee.manager == True:
		# 			return [('status', '=', 'hr')]
		# 		if employee.name==True:
		# 			return [('status','=','done')]
				

		

	# @api.('replay_message')
	# def sending_email(self):
	# 	template = self.env.ref('bi_hr.help_desk_mail')
	# 	self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
		
	@api.onchange('name')
	def get_details_from_employee(self):
		desk_details=self.env['hr.employee'].search([])
		for x in desk_details:
			if self.name.name==x.name:
				self.mobile=x.mobile_phone
				self.email=x.work_email
				self.designation=x.job_id.name
			





	
		
				

class help_desk_department(models.Model):
	_name='hr.help_department'
	name = fields.Char('Department',required=True)
