from odoo import api, fields, models

class ProjectTaskLogWork(models.TransientModel):
    _name = "project.task.log.work"

    user_id = fields.Many2one('res.users', compute='_compute_user_id', readonly=False)
    date = fields.Date('Date', required=True, index=True, default=fields.Date.context_today)
    log_time = fields.Float('Time', default=0.0)
    
    @api.model
    def default_get(self, field_list):
        result = self.env['account.analytic.line'].default_get(field_list)
        if not self.env.context.get('default_employee_id') and 'employee_id' in field_list and result.get('user_id'):
            result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', result['user_id']), ('company_id', '=', result.get('company_id', self.env.company.id))], limit=1).id
        return result

    def _domain_employee_id(self):
        if not self.user_has_groups('hr_timesheet.group_hr_timesheet_approver'):
            return [('user_id', '=', self.env.user.id)]
        return []
        
    employee_id = fields.Many2one('hr.employee', "Employee", domain=_domain_employee_id, context={'active_test': False})
    comment = fields.Char(required=True)
    description = fields.Html(string='Description')

    @api.depends('employee_id')
    def _compute_user_id(self):
        for line in self:
            def_user = self.env['account.analytic.line']._default_user()
            user_id = line.employee_id.user_id if line.employee_id else def_user
            line.user_id = user_id

    def action_log_work_apply(self):
        tasks = self.env['project.task'].browse(self.env.context.get('active_ids'))
        for task in tasks:
            if self.description:
                task.message_post(body=self.description)
            vals_list = {
                    'name': self.comment if self.comment else ' / ',
                    'date': self.date,
                    'unit_amount': self.log_time,
                    'task_id': task.id,
                    'project_id': task.project_id.id,
                    'user_id': self.user_id.id,
                    'employee_id': self.employee_id.id
                }
            self.env['account.analytic.line'].create(vals_list)
