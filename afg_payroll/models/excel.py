from odoo import api, fields, models, _
import xlwt, xlsxwriter
import base64


class EmployeeInfoExcelReport(models.TransientModel):
    _name = 'employee.salary.payslip.report'
    _description = 'Employee Information Excel Report'

    employee_id = fields.Many2one('hr.afg.payroll.batches', string='Batches', required=True)

    @api.multi
    def generated_excel_report(self, record):
        
        employee_obj = self.env['hr.afg.payroll'].search([])
        
        workbook = xlwt.Workbook()

        # Style for Excel Report
        style0 = xlwt.easyxf('font: name Times New Roman bold on; align: horiz left; borders: top double; pattern: pattern solid, fore_colour white', num_format_str='#,##0.00')
        style1 = xlwt.easyxf('font:bold True, color Yellow , height 400;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour blue;', num_format_str='#,##0.00')
        style2 = xlwt.easyxf('font:bold True, color White , height 440;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour  gold;', num_format_str='#,##0.00')
        styletitle = xlwt.easyxf(
            'font:bold True, color White, height 240;  borders: top double; align: horiz center; pattern: pattern solid, fore_colour gold;',
            num_format_str='#,##0.00')
        sheet = workbook.add_sheet("Employee Payslip Report")

        # sheet.write_merge(0, 0, 0, 10, 'GENERAL INFORMATION', style2)

        # sheet.write_merge(1, 1, 0, 5, 'Contact Information', style1)
        # sheet.write_merge(1, 1, 6, 10, 'Position', style1)

        sheet.write(2, 0, 'Employee Name', styletitle)
        sheet.write(2, 1, 'Mobile', styletitle)
        sheet.write(2, 2, 'Campus', styletitle)
        sheet.write(2, 3, 'Department', styletitle)
        sheet.write(2, 4, 'Designation', styletitle)
        sheet.write(2, 5, 'Base Salary', styletitle)
        sheet.write(2, 6, 'Loss Of Pay', styletitle)
        sheet.write(2, 7, 'Bonus', styletitle)
        sheet.write(2, 8, 'Net Pay', styletitle)
        sheet.write(2, 9, 'Tax', styletitle)
        sheet.write(2, 10, 'Advance Salary', styletitle)
        sheet.write(2, 11, 'Security Deposite', styletitle)
        sheet.write(2, 12, 'Other Deductions', styletitle)
        sheet.write(2, 13, 'Salary Payble', styletitle)

        sheet.col(0).width = 700 * (len('Employee Name') + 1)
        sheet.col(1).width = 700 * (len('Mobile') + 1)
        sheet.col(2).width = 700 * (len('Campus') + 1)
        sheet.col(3).width = 700 * (len('Department') + 1)
        sheet.col(4).width = 700 * (len('Designation') + 1)
        sheet.col(5).width = 700 * (len('Base Salary') + 1)
        sheet.col(6).width = 700 * (len('Loss Of Pay') + 1)
        sheet.col(7).width = 700 * (len('Bonus') + 1)
        sheet.col(8).width = 700 * (len('Net Pay') + 1)
        sheet.col(9).width = 700 * (len('Tax') + 1)
        sheet.col(10).width = 700 * (len('Advance Salary') + 1)
        sheet.col(11).width = 700 * (len('Security Deposite') + 1)
        sheet.col(12).width = 700 * (len('Other Deductions') + 1)
        sheet.col(13).width = 700 * (len('Salary Payble') + 1)
       
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 256 * 2
        sheet.row(1).height = 256 * 2
        sheet.row(2).height = 256 * 2

        row = 3
        for rec in employee_obj:
            
            sheet.write(row, 0, rec.employee_id.name, style0)
            sheet.write(row, 1, rec.mobile, style0)
            sheet.write(row, 2, rec.campus, style0)
            sheet.write(row, 3, rec.department, style0)
            sheet.write(row, 4, rec.designation, style0)
            sheet.write(row, 5, rec.base_salary, style0)
            sheet.write(row, 6, rec.lop, style0)
            sheet.write(row, 7, rec.bonus, style0)
            sheet.write(row, 8, rec.net_pay, style0)
            sheet.write(row, 9, rec.tax, style0)
            sheet.write(row, 10, rec.advance_salary, style0)
            sheet.write(row, 11, rec.security_deposite, style0)
            sheet.write(row, 12, rec.other_deductions, style0)
            sheet.write(row, 13, rec.salary_payable, style0)
        
            row +=1
        workbook.save('/tmp/employee_info_list.xls')
        result_file = open('/tmp/employee_info_list.xls', 'rb').read()
        attachment_id = self.env['wizard.payslip.details.report'].create({
            'name': 'Employee Payslips Batchwise.xls',
            'report': base64.encodestring(result_file)
        })

        return {
            'name': _('Notification'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.payslip.details.report',
            'res_id': attachment_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


class WizardEmployeeInformationExcelReport(models.TransientModel):
    _name = 'wizard.payslip.details.report'

    name = fields.Char('File Name', size=64)
    report = fields.Binary('Prepared File', filters='.xls', readonly=True)
