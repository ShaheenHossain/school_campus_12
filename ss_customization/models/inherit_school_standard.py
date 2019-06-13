# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

class SchoolTeacher(models.Model):
    _inherit = 'school.teacher'
    
    examiner_program_id = fields .Many2one('standard.standard',"Program")
    examiner_is_shift = fields.Selection(related='examiner_program_id.is_shift', store=True)
    examiner_medium_id = fields.Many2one('standard.medium', 'Shift')
    examiner_semester_id = fields.Many2one('standard.semester',"Course Level")
    examiner_room_no = fields.Many2one('standard.division',"Room No")
    start_time = fields.Datetime(string="Start Date")
    end_time = fields.Datetime(string="End Date")


class StudentTimetableRegular(models.Model):
    _name = 'student.timetable.regular'
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    campus = fields.Many2one('school.school','Campus')
    program_id = fields.Many2one('standard.standard', string="Program")

    def print_report(self):
        data = {}
        class_lines = self.env['school.standard'].search([('school_id','=',self.campus.id),('standard_id','=',self.program_id.id),('start_date','=',self.start_date),('end_date','=',self.end_date)])
        data['class']= class_lines.ids
        data['active_model']='school.standard'
        print ("==============class+lines",class_lines.ids)
        return self.env['report'].get_action(self, 'ss_customization.report_student_timetable', data=data)

    def print_report_excel(self):
        class_lines = self.env['school.standard'].search([('school_id','=',self.campus.id),('standard_id','=',self.program_id.id),('start_date','=',self.start_date),('end_date','=',self.end_date)])
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("TimeTable")
        fields_dict = {}
        worksheet.write(0,0,'Teacher')
        worksheet.write(0,1,'Class')
        worksheet.write(0,2,'Room No')
        worksheet.write(0,3,'Semester')
        worksheet.write(0,4,'Start Date')
        worksheet.write(0,5,'End Date')
        worksheet.write(0,6,'Spend Days')
        
        row=0
        col=1
        for i in class_lines:
            worksheet.write(col,row, i.teacher_id.name)
            worksheet.write(col,row+1, i.standard)
            worksheet.write(col,row+2, i.division_id.name)
            worksheet.write(col,row+3, i.semester_id.name)
            worksheet.write(col,row+4, i.start_date)
            worksheet.write(col,row+5, i.end_date)
            worksheet.write(col,row+6, (datetime.strptime(self.end_date, '%Y-%m-%d') - datetime.strptime(self.start_date, '%Y-%m-%d')).days + 1)
            col+=1
        file_data = cStringIO.StringIO()
        workbook.save(file_data)
        res = self.env['timetable.export'].create({
            'data': base64.encodestring(file_data.getvalue()),
            'name': "TimeTable.xls"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'TimeTable',
            'res_model': 'timetable.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': res.id,
            'target': 'new'
        }
class timetable_export(models.TransientModel):
    _name = "timetable.export"
 
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)

    


class SchoolStandard(models.Model):
    _inherit = 'school.standard'

    teacher_id = fields.Many2one('school.teacher', string="Teacher")
    
    @api.onchange('teacher_id')
    def onchange_teacher_id(self):
        class_ids = self.search([('teacher_id','=',self.teacher_id.id)]) 
        print ("============class_ids",class_ids)
        for data in class_ids:
            print ("============data.start_date  <= self.start_date <= data.end_date and data.start_date  <= self.end_date <= data.end_date:",data.start_date  <= self.start_date <= data.end_date and data.start_date  <= self.end_date <= data.end_date)
            if data.start_date  <= self.start_date <= data.end_date or data.start_date  <= self.end_date <= data.end_date:
                raise UserError('This teacher is allocated for another class')
            

    @api.multi
    def _cron_start_stop(self):
        running_class_ids = self.search([('start_date','=',fields.Date.today())])
        running_class_ids.update({
            'state':'running'
            })
        close_class_ids = self.search([('end_date','=', fields.Date.today())])
        close_class_ids.update({'state':'close'})
        return

class StudentFeedback(models.Model):
    _name = 'student.feedback'

    student_id = fields.Many2one('student.student', string="Student")
    feedback = fields.Text('Feedback')

    @api.model
    def default_get(self,vals):
        print ("=============context",self._context)
        res = super(StudentFeedback, self).default_get(vals)
        if self._context.get('active_id'):
            res['student_id'] = self._context.get('active_id')
        return res
    
    @api.multi
    def send_main_feedback(self):
        if not self.student_id.email:
            raise UserError('Please Register your email ID')
        template_obj = self.env['mail.template'].sudo().search([('name','=','Feedback From Student')], limit=1)
        print ("===========template_obj",template_obj)
        str = 'Student Name:' + self.student_id.name +'<br/> Class:'+ self.student_id.standard_id.standard+ '<br/> Program:'+ self.student_id.program_id.name+'<br/> Shift:'+ self.student_id.medium_id.name+'<br/> Feedback:'+ self.feedback+'</td></tr></table>'
        emails = []
        users = self.env['student.feedback.setting'].search([],limit=1,order='id desc')
        if users.user_ids:
            for email in users.user_ids:
                emails.append(email.partner_id.email)
        
            if template_obj:
             mail_values = {
              'subject': template_obj.subject,
              'body_html': str,
              'email_to':",".join(emails),
              'email_from': self.env['res.users'].browse(self._uid).partner_id.email
             }
             create_and_send_email = self.env['mail.mail'].create(mail_values).send()  
             print ("==============create_and_send_email",create_and_send_email)
        else:
            raise UserError('Configuration email does not added contact to your administaration')

class StudentFeedbackSetting(models.Model):
    _name = 'student.feedback.setting'
    

    @api.model
    def default_get(self,vals):
        search = self.search([],limit=1,order='id desc')
        res = super(StudentFeedbackSetting, self).default_get(vals)
        print ("==============search",search)
        if search:
            res['user_ids'] = search.user_ids.ids
        return res

    user_ids = fields.Many2many('res.users')
        