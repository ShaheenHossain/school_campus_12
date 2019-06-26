from odoo import api, fields, models,_


class HrRecruitmentInherit(models.Model):
	_inherit = 'hr.applicant'


	state = fields.Selection([
							('draft','Shortlisted'),
							('pit','Personal Information Round'),
							('written_test','Written Test'),
							('technical_round','Technical Round'),
							('demo','Demo/AM'),
							('hr_round','Hr Round'),
							('refuse','Refuse'),
							('done','Done')],string='Stages', readonly=True, copy=False, index=True, 
							track_visibility='onchange', default='draft')
	current_round = fields.Char(string="Current Round")
	next_round = fields.Char(string="Next Round")


	@api.multi
	def draft_pit_action(self):
		self.write({'state':'pit'})

	@api.multi
	def pit_written_action(self):
		self.current_round = self.state
		self.write({'state':'written_test'})
		self.next_round = self.state
		self.interview_rounds_email_notification()

	@api.multi
	def written_techncal_action(self):
		self.current_round = self.state
		self.write({'state':'technical_round'})
		self.next_round = self.state
		self.interview_rounds_email_notification()
		
	@api.multi
	def written_demo_action(self):
		self.current_round = self.state
		self.write({'state':'demo'})
		self.next_round = self.state
		self.interview_rounds_email_notification()

		

	@api.multi
	def technical_demo_hr_action(self):
		self.current_round = self.state
		self.write({'state':'hr_round'})
		self.next_round = self.state
		self.interview_rounds_email_notification()
		

	@api.multi
	def hr_done_action(self):
		self.write({'state':'done'})

	@api.multi
	def refuse_action(self):
		self.write({'state':'refuse'})

	@api.multi
	def interview_rounds_email_notification(self):
		template = self.env.ref('bi_hr.recruitment_stage_email_template')
		self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
