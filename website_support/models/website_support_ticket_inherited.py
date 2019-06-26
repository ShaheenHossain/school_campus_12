from openerp import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError
import os, sys



#Developer2 For Online Enquiries
class Enquiries_inherited(models.Model):
	_inherit = ["website.support.ticket"]



	name = fields.Char(string="Name",required=True)
	country = fields.Many2one('res.country',string="Country")
	message = fields.Text(string="Message",required=True)
	ticket_no = fields.Char(string="Enquiry No.",required=True, Index= True, default=lambda self:('New'), readonly=True)
	status = fields.Selection([('draft','Draft'),('followup','Followup'),('add-application','Add-Application')],default="draft")
	campus_name = fields.Many2one('school.school',string="Campus-Name")
	address = fields.Char(string="Address")
	# ids=fields.Char(string='Code',compute='_compute_display_name')




	@api.multi
	def name_get(self):
		res = super(Enquiries_inherited, self).name_get()
		result=[]
		for x in self:
			display_value=""
			display_value += x.name or ""
			display_value += ' ['
			display_value += x.ticket_no or ""
			display_value += ']'
			print display_value,"4444444444444444444444"

			
		 	result.append((x.id,display_value))
		return result




	@api.model
	def create(self, vals):
		if vals.get('ticket_no', _('New')) == _('New'):
			vals['ticket_no',] = self.env['ir.sequence'].next_by_code('enquiry.view.id') or _('New')
			# rr=vals['name']=str(vals['name'])+''str(ff)
			
			result = super(Enquiries_inherited, self).create(vals)
			return result

	@api.multi
	def enquiry_status(self):

		self.write({"status":"followup"})
	@api.multi
	def application_status(self):
		self.write({"status":"add-application"})

	@api.constrains('email')
	def email_validating(self):
		for x in self:
			if re.match(r"^[a-zA-Z0-9][\w-]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$",x.email)==None:
				raise ValidationError("Please Provide valid Email Address: %s" % x.email)






	@api.constrains('mobile')	
	def mobile_validation(self):
		for x in self:
			if len(str(x.mobile))==10:
				res=re.match(r"^0[0-9]{1,10}$",x.mobile)
				if res:
					return True
				else:
					raise UserError(_("Please Check your Valid  Mobile Number"))
			else:
				raise UserError(_("Your Mobile Number Having More than 10 Digits"))


	@api.constrains('name')
	def name_validation_firstname(self):
		for y in self:
			if len(y.name)>=3:
				res=re.match(r"^[^\W0-9_]+([ \-'][^\W0-9_]+)*?$",y.name)
				if res:
					return True
				else:
					raise UserError(_("Your First name must be have Only character"))
			else:
				raise UserError(_("Your first name must be more than 3 Characters"))
	@api.constrains('last_name')
	def name_validation(self):
		for y in self:
			if len(y.last_name)>=3:
				res=re.match(r"^[^\W0-9_]+([ \-'][^\W0-9_]+)*?$",y.last_name)
				if res:
					return True
				else:
					raise UserError(_("Your Last name must be have Only character"))
			else:
				raise UserError(_("Your last name must be more than 3 Characters"))
	# @api.model
 #    def create(self, vals):
 #        vals['name'] = self.env['ir.sequence'].next_by_code('website.support.ticket')
 #        return super(Enquiries_inherited, self).create(vals)


	
	


















	
	@api.constrains('last_name')
	def name_validation(self):
		for y in self:
			if len(y.last_name)>=3:
				return True
			else:
				raise UserError(_("Your name must be more than 3 Characters"))

	