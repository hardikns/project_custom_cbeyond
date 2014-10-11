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
from openerp.osv import osv, fields
from openerp.tools.safe_eval import safe_eval
import base64


class task_analysis_report(osv.osv_memory):
    """ Task Analysis Report Wizard"""

    _name = 'task.analysis.report'

    _columns = {
        'groupby_all':fields.char('Group By value', size=200, ),
        'groupby':fields.selection([
                ('project_id','Project'),
                ('name','Task'),
                ('partner_id','Contact'),
                ('user_id','Assigned To'),
                ('day','Day'),
                ('month','Month'),
                ('year','Year'),
                 ],    'Group By', ),
        'csvfile': fields.binary('CSV File', readonly=True),
        'csv_filename' : fields.char('CSV File Name', size=40),
              
    }
    _defaults = {
        'csv_filename' : "task_analysis_report.csv",
    }

    def return_data(self, ids):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'task.analysis.report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
        }           
    # No Longer Used 
    def add_groupby(self, cr, uid, ids, context=None): 
        vals = {}
        for data in self.browse(cr, uid, ids, context=context):
            groupby_all = data.groupby_all and safe_eval(data.groupby_all) or []
            print groupby_all
            groupby_all.append(data.groupby)
            vals['groupby_all'] = str(groupby_all)
            vals['groupby'] = False 
        self.write(cr, uid, ids, vals, context=context)
        return self.return_data(ids)
    # No Longer Used
    def clear_groupby(self, cr, uid, ids, context=None): 
        vals = {}
        vals['groupby_all'] = False
        vals['groupby'] = False 
        self.write(cr, uid, ids, vals, context=context)
        return self.return_data(ids)

    def generate_report(self,cr, uid, ids, context=None):
#         sql2 = """
#                select %s
#                sum(nbr),
#                sum(no_of_days),
#                sum(total_hours),
#                sum(hours_planned),
#                sum(remaining_hours),
#                sum(hours_effective),
#                sum(hours_delay),
#                avg(opening_days),
#                avg(closing_days),
#                avg(delay_endings_days),
#                avg(progress)
#                from report_project_task_user
#                %s
#                """
#         data = self.browse(cr, uid, ids, context=context)[0]
        groupby_list = ['project_id']
#         if data.groupby_all:
#             groupby_list = safe_eval(data.groupby_all)
#             assert isinstance(groupby_list, list)
#         sql = sql2 % (','.join(groupby_list)+',','GROUP BY '+','.join(groupby_list))
#         cr.execute(sql)
#         res = cr.fetchall()
        
        rpt_pool = self.pool.get('report.project.task.user')
        fieldlist = ['nbr','no_of_days','total_hours','hours_planned','remaining_hours','hours_effective',
                     'hours_delay','opening_days','closing_days','delay_endings_days','progress']
        res1 = rpt_pool.read_group(cr, uid, [], groupby_list+fieldlist, groupby_list)

        csv = unicode(','.join(groupby_list) + ",# of tasks,# of Days,Total Hours,Planned Hours,Remaining Hours,Effective Hours,Avg. Planned - Effective,Days to Open,Days to Close,Overpassed Deadline,Progress ")
        for row in res1:
            row_list = []
            for field in groupby_list+fieldlist:
                if isinstance(row[field], tuple):
                    val = unicode(row[field][1])
                else:
                    val = unicode(row[field])
                row_list = row_list + [val] 
            #row_list = [item and str(item) or "0" for item in list(row)]
            csv = csv + u'\r\n' + u','.join(row_list)
        try: 
            self.write(cr, uid, ids, {'csvfile': base64.encodestring(csv.encode('cp1250','replace'))},context=context)
        except:
            self.write(cr, uid, ids, {'csvfile': base64.encodestring(csv.encode('utf-8','replace'))},context=context)
        return self.return_data(ids)        
        
task_analysis_report()
