
from openerp.osv import osv, fields
import base64
import datetime

class analytical_timesheet_employees(osv.osv_memory):
    _name = 'hr.analytical.timesheet.users'
    _inherit = 'hr.analytical.timesheet.users'
    
    _columns = {
        'csvfile': fields.binary('CSV File', readonly=True),
        'allemps': fields.boolean('Select All Employees'),
        'csv_filename' : fields.char('CSV File Name', size=40),
    }
    
    _defaults = {
        'csv_filename' : "Employees_timesheet_report.csv",
    }
    
    def onchange_allemps(self, cr, uid, ids, allemps, context=False):
        res={}
        emp_pool = self.pool.get('hr.employee')
        empids = emp_pool.search(cr, uid, [], context=context)
        res['employee_ids'] = empids
        res['allemps'] = False
        return {'value':res}
    
    def download_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        som = datetime.date(data['year'], data['month'], 1).strftime('%Y-%m-%d')
        eom1 = datetime.date(data['year'], data['month']+1, 1).strftime('%Y-%m-%d')
        
        cr.execute("""select aa.name, 
                      p.external_id,
                      ph.name,
                      t.name,
                      ph.effort_capatilized,
                      p.cpr_code,
                      e.name_related,
                      e.ext_code,
                      e.emp_type,
                      e.cost_center,
                      l.date,
                      sum(l.unit_amount)
                      from project_project p, 
                      project_phase ph, 
                      project_task t,
                      hr_employee e,
                      account_analytic_line l, 
                      hr_analytic_timesheet ts,
                      account_analytic_account aa,
                      resource_resource rr
                      where l.date >= %s
                      and l.date < %s
                      and l.user_id = rr.user_id
                      and rr.id = e.resource_id                         
                      and l.id = ts.line_id
                      and ts.task_id = t.id
                      and t.project_id = p.id
                      and p.analytic_account_id = aa.id
                      and t.phase_id = ph.id
                      and l.unit_amount > 0.0
                      and e.id in %s
                      Group by aa.name, 
                      p.external_id,
                      ph.name,
                      t.name,
                      ph.effort_capatilized,
                      p.cpr_code,
                      e.name_related,
                      e.ext_code,
                      e.emp_type,
                      e.cost_center,
                      l.date""", (som, eom1, tuple(data['employee_ids']),))

        rows = cr.fetchall()
        csv_data = unicode("Month,Project,Cbeyond Project Id,Phase,Task,Capex?,CPR Code,Employee,Emp Code,Employee type,Cost Center,Date,Hours")
        month_str = unicode(datetime.date(data['year'], data['month'], 1).strftime('%Y%m'))
        for row in rows:
            csv_row = month_str + u',' + u','.join([unicode(item) for item in list(row)])
            csv_data = csv_data + u'\r\n' + csv_row
        try:
            self.write(cr, uid, ids, {'csvfile': base64.encodestring(csv_data.encode('cp1250','replace'))},context=context)
        except:
            self.write(cr, uid, ids, {'csvfile': base64.encodestring(csv_data.encode('utf-8','replace'))},context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.analytical.timesheet.users',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
        }
        
analytical_timesheet_employees()

