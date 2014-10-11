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
from openerp.osv import orm, fields

class project_from_tempalte(orm.TransientModel):
    _name = "project.from.template"
    _description = "Create Project from Project Template via Wizard"
    
    _columns = {
        'project_id': fields.many2one('project.project', "Template Project", 
                                      domain=[('state','=','template')], required=True),
        'project_name': fields.char("New Project Name", size=64, required=True),
    }
    
    def create_project(self,cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids, context=context)[0]
        t_project_id = data.project_id.id
        project_pool = self.pool.get('project.project')
        res = project_pool.duplicate_template(cr, uid, [t_project_id], context=context)
        new_project_id = res.get('res_id',False)
        if new_project_id:
            project_pool.write(cr, uid, [new_project_id],{'name':data.project_name})
        return res
