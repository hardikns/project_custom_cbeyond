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
from openerp.osv import orm , fields

class resource_resource(orm.Model):
    _inherit = "resource.resource"
    
    _sql_constraints = [('user_id_unique', 'unique (user_id)', 'The user is already linked to an employee'),      ]

resource_resource()

class hr_employee(orm.Model):
    _name="hr.employee"
    _inherit="hr.employee"
    _columns = {
        'ext_code': fields.char("Employee/Contrator ID", size=40, help="External Id used to identify the Employee or Contractor"),
        'emp_type': fields.selection([('employee','Employee'),
                                      ('contractor','Contractor'),
                                      ('contractor-nr','Contractor No Reporting')], 
                                     "Employee Type", required=True),
        'cost_center' : fields.char('Cost Center Code', size=40),        
    }
    _defaults = {
        'emp_type': 'employee',
    }
hr_employee()