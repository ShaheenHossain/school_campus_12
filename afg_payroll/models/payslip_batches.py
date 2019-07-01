import time
from datetime import datetime, timedelta
from dateutil import relativedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class VrPayslipBatches(models.Model):
	_name = "hr.afg.payroll.batches"


	name = fields.Char(required=True, readonly=True, states={'draft': [('readonly', False)]})
	slip_ids = fields.One2many('hr.afg.payroll', 'payslip_run_id', string='Payslips', readonly=True,
		states={'draft': [('readonly', False)]})
	state = fields.Selection([
		('draft', 'Draft'),
		('close', 'Close'),
		('done', 'Done'),
		], string='Status', index=True, readonly=True, copy=False, default='draft')
	date_start = fields.Date(string='Date From', required=True, readonly=True,
		states={'draft': [('readonly', False)]}, default=time.strftime('%Y-%m-01'))
	date_end = fields.Date(string='Date To', required=True, readonly=True,
		states={'draft': [('readonly', False)]},
		default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
	credit_note = fields.Boolean(string='Credit Note', readonly=True,
		states={'draft': [('readonly', False)]},
		help="If its checked, indicates that all payslips generated from here are refund payslips.")
