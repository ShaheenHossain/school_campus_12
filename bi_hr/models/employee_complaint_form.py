import datetime
from datetime import datetime
from odoo.exceptions import UserError
import re

from odoo import fields, api,models,_



class employee_complaint_form(models.Model):
	_name = 'hr.employee_complaint'


	@api.model
	def _default_employee_name(self):
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id


	name=fields.Many2one('hr.employee',string="Name",required=True,default=_default_employee_name,readonly=True)
	email = fields.Char(string="Email")
	phone = fields.Char(string="Phone Number")
	job_title = fields.Char(string='Current Job Title')
	dep = fields.Char(string='Department')
	campus_name = fields.Char(string="Campus Name")
	work_from =fields.Date(string='How long have you worked for MELI?')
	previous_complaint=fields.Selection([('yes','Yes'),('no','No')],default='no',string="Have you filed an official complaint with any other HOD/AAM earlier?")
	yes_action=fields.Char(string="If YES, with whom was the action commenced?")
	yes_action2=fields.Char(string="At what stage is this action?")
	complaint_discuss=fields.Selection([('yes','Yes'),('no','No')],default='no',string="Have you attempted to resolve this matter by discussing it with someone else?")
	discuss_action1=fields.Char(string="If YES, please provide details:")
	status=fields.Selection([('draft','Draft'),('confirm','Confirm'),
							 ('it','IT'),
							 ('hr','HR'),
							 ('gravience','Gravience'),
							 ('in progress','In Progress'),
							 ('solved','Solved'),
							 ('cancel','Cancel'),
							 ('closed','Closed')],default="draft")
	issue_of_dep=fields.Selection([('hr','HR'),('it','IT'),
							 ('gravience','Gravience')],string="Issue Of Department",required=True)

	name1=fields.Char(string="Name")
	dep1 = fields.Char(string='Department')
	title = fields.Char(stiring='Title')
	work_location = fields.Char(stiring='Work Location')

	remarks = fields.Text(string="Remarks")
	issue_date=fields.Date(string="Compliant-Date",readonly=True)
	solved_date=fields.Date(string='Solved-Date',readonly=True)
	description=fields.Text(string="GENERAL NATURE OF COMPLAINT",required=True)

	# it_remarks = fields.Char(string="IT Remarks")
	# gravience_remarks = fields.Char(string="Gravience Remarks")



	

	@api.onchange('name')
	def geting_details(self):
		if self.name:
			self.email=self.name.work_email
			self.phone=self.name.mobile_phone
			self.job_titile=self.name.job_id.name
			self.dep=self.name.department_id.name


	@api.multi
	def send_to_hr(self):
		self.issue_date=datetime.now()
		self.write({'status':'hr'})

	@api.multi
	def send_to_it(self):
		self.issue_date=datetime.now()
		self.write({'status':'it'})

	@api.multi
	def send_to_gravience(self):
		self.issue_date=datetime.now()
		self.write({'status':'gravience'})


	@api.multi
	def solved(self):
		self.write({'status':'in progress'})
		# if self.status=='hr':
		# 	self.write({'status':'in progress'})
		# if self.status=='it':
		# 	self.write({'status':'in progress'})
		# if self.status=='gravience':
		# 	self.write({'status':'in progress'})


	@api.multi
	def confirmation_complaint(self):
		self.write({'status':'confirm'})

	@api.multi
	def complaint_solution(self):
		self.solved_date=datetime.now()
		self.write({'status':'solved'})

	@api.multi
	def closed_complaints(self):
		self.write({'status':'closed'})
	@api.multi
	def cancel(self):
		self.write({'status':'cancel'})


	

	



