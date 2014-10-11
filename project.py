# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp import tools

class project(osv.Model):
    _name='project.project'
    _inherit='project.project'
    
    _columns={
        'external_id': fields.char("Cbeyond Project Id", size=40, 
                                   help="CWE Code in JIRA system", 
                                   required=True, readonly=True, 
                                   states={'template':[('required',False),('readonly',False)], 
                                           'open':[('required',True),('readonly',False)]}
                                   ),
        'cpr_code': fields.char("CPR Code", size=40, help="CPR code", 
                                readonly=True, required=True, 
                                states={'template':[('required',False),('readonly',False)], 
                                        'open':[('required',True),('readonly',False)]}
                                ),
    }
    _defaults = {
        'use_phases':True,
    }
   
    def map_tasks(self, cr, uid, old_project_id, new_project_id, context=None):
        """ copy and map tasks from old to new project """
        if context is None:
            context = {}
        map_task_id = {}
        map_phase_id = {}
        task_obj = self.pool.get('project.task')
        phase_obj = self.pool.get('project.phase')
        proj = self.browse(cr, uid, old_project_id, context=context)
        for phase in proj.phase_ids:
            map_phase_id[phase.id] = phase_obj.copy(cr, uid, phase.id, {'project_id':new_project_id,
                                                                        'task_ids':[],
                                                                        'name':phase.name}, 
                                          context=context)
        for task in proj.tasks:
            map_task_id[task.id] =  task_obj.copy(cr, uid, task.id, 
                                                  {'project_id':new_project_id, 
                                                    'phase_id':map_phase_id[task.phase_id.id]}, 
                                                  context=context)
        task_obj.duplicate_task(cr, uid, map_task_id, context=context)
        return True

    def copy(self, cr, uid, ids, default=None, context=None):
        if context is None:
            context = {}
        if default is None:
            default = {}
        default['phase_ids'] = []    
        res = super(project, self).copy(cr, uid, ids, default, context)
        return res
        

project()

class project_phase(osv.Model):
    _name='project.phase'
    _inherit='project.phase'
    
    def _get_default_uom(self,cr, uid, context=None):
        uom_ids = self.pool.get('product.uom').search(cr, uid, [('name', 'ilike', 'Day(s)')])
        if len(uom_ids):
            return uom_ids[0]
        return False
        
    _columns={
        'effort_capatilized': fields.boolean("Effort Capatilized?", readonly=True,states={'draft':[('readonly',False)]} ),
    }
    
    _defaults= {
        'effort_capatilized': False,
        'product_uom': _get_default_uom,
    }    
project_phase()

class report_project_task_user(osv.Model):
    _name="report.project.task.user"
    _inherit="report.project.task.user"

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'report_project_task_user')
        cr.execute("""
            CREATE view report_project_task_user as
              SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                    to_char(t.date_start, 'YYYY') as year,
                    to_char(t.date_start, 'MM') as month,
                    to_char(t.date_start, 'YYYY-MM-DD') as day,
                    date_trunc('day',t.date_start) as date_start,
                    date_trunc('day',t.date_end) as date_end,
                    to_date(to_char(t.date_deadline, 'dd-MM-YYYY'),'dd-MM-YYYY') as date_deadline,
--                    sum(cast(to_char(date_trunc('day',t.date_end) - date_trunc('day',t.date_start),'DD') as int)) as no_of_days,
                    abs((extract('epoch' from (t.date_end-t.date_start)))/(3600*24))  as no_of_days,
                    t.user_id,
                    t.progress as progress,
                    t.project_id,
                    t.state,
                    t.effective_hours as hours_effective,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    a.partner_id,
                    t.stage_id,
                    t.remaining_hours as remaining_hours,
                    t.total_hours as total_hours,
                    t.delay_hours as hours_delay,
                    t.planned_hours as hours_planned,
                    (extract('epoch' from (t.date_end-t.create_date)))/(3600*24)  as closing_days,
                    (extract('epoch' from (t.date_start-t.create_date)))/(3600*24)  as opening_days,
                    abs((extract('epoch' from (t.date_deadline-t.date_end)))/(3600*24))  as delay_endings_days
              FROM project_task t, 
                   project_project p,
                   account_analytic_account a 
                WHERE t.active = 'true' 
                and t.project_id = p.id
                and p.analytic_account_id = a.id
                GROUP BY
                    t.id,
                    remaining_hours,
                    t.effective_hours,
                    progress,
                    t.total_hours,
                    t.planned_hours,
                    hours_delay,
                    year,
                    month,
                    day,
                    t.create_date,
                    t.date_start,
                    t.date_end,
                    date_deadline,
                    t.user_id,
                    t.project_id,
                    t.state,
                    t.priority,
                    t.name,
                    t.company_id,
                    a.partner_id,
                    t.stage_id

        """)
    
report_project_task_user()