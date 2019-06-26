# -*- coding: utf-8 -*-
import datetime

import calendar
import babel
from odoo.tools.safe_eval import safe_eval
from odoo import models, fields, api,_

class payroll_details(models.Model):
	_name = 'hr.afg.payroll'




	sequence=fields.Char(string="Sequence No", required=True, Index= True, default=lambda self:('New'), readonly=True)
	employee_id = fields.Many2one('hr.employee',string="Employee Name")
	mobile=fields.Char(string="Mobile")
	email =fields.Char(string="email")
	date_of_join=fields.Date(string="Date Of Join")
	campus =fields.Char(string="Campus")
	department=fields.Char(string="Department")
	designation=fields.Char(string="Designation")
	start_date=fields.Date(string="Start Date")
	end_date=fields.Date(string="End Date")
	emp_salary=fields.Char(string="Salary")
	days=fields.Char(string="Days")
	name=fields.Char(string="Payslip Name")
	approved_leaves=fields.Char(string="Leaves")




	@api.onchange('employee_id')
	def get_employee_details(self):
		if self.employee_id:
			self.mobile=self.employee_id.mobile_phone
			self.email=self.employee_id.work_email
			self.date_of_join=self.employee_id.date_of_join
			self.campus=self.employee_id.school_id.name
			self.department=self.employee_id.department_id.name
			self.designation=self.employee_id.job_id.name
			rec=self.env['hr.contract'].search([('employee_id','=',self.employee_id.name)])
			self.emp_salary=rec.offered_salary
			date = datetime.date.today()
			start_date = datetime.datetime(date.year, date.month, 1)
			end_date = datetime.datetime(date.year, date.month, calendar.mdays[date.month])
		 	self.start_date=start_date
		 	self.end_date=end_date
			day = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%d')
			year = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').strftime('%Y')
			self.days=day
			# ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.start_date, "%Y-%m-%d")))
   #      	locale = self.env.context.get('lang') or 'en_US'
   			mydate = datetime.datetime.today()
			dee=mydate.strftime("%B")
			if self.employee_id !=False:
				self.name = _('Salary Slip of %s for %s %s') % (self.employee_id.name,dee,year)

			rec=self.env['hr.holidays'].search([('employee_id','=',self.employee_id.name)])
			print self.start_date,"555555555555",self.end_date,"666666666666"
			for obj in rec:
				print obj.date_from,"kkkkkkkk",obj.date_to
		
				if self.start_date<=rec.date_from and self.end_date>=rec.date_to:
					print obj.number_of_days_temp,"666666666666666666666666666"
	
	


	@api.model
	def create(self, vals):
		if vals.get('sequence', _('New')) == _('New'):
			vals['sequence'] = self.env['ir.sequence'].next_by_code('hr.afg.payroll') or _('New')
			result = super(payroll_details, self).create(vals)
			return result





