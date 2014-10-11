
from openerp.osv import osv
from openerp.tools.translate import _

class hr_timesheet_sheet(osv.osv):
    _name = "hr_timesheet_sheet.sheet"
    _inherit = "hr_timesheet_sheet.sheet"
    
    def create(self, cr, uid, vals, *args, **argv):
        if 'employee_id' in vals:
            if (self.pool.get('hr.employee').browse(cr, uid, vals['employee_id']).emp_type 
                not in ['employee','contractor']):
                raise osv.except_osv(_('Error!'), _('In order to create a timesheet for this employee, change the employee type to Employee or Contractor.'))
                
        return super(hr_timesheet_sheet, self).create(cr, uid, vals, *args, **argv)
