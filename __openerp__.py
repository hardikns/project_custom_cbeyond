# -*- encoding: utf-8 -*-
##############################################################################
#
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
{'name' : 'Project Customizations for Cbeyond',
 'version' : '0.12',
 'author' : 'Msys',
 'maintainer': 'Msys',
 'category': 'Human Resources',
 'depends' : ['hr_taskbased_timesheet'],
 'description': """
 
    This module contains customizations at for Project/Timesheet modules which are specific to Cbeyond
    
    """,
 'website': 'http://www.msys-tech.com',
 'data': [
          'cbeyond_custom.xml', 
          'wizard/employees_timesheet_report.xml',
          'wizard/task_analysis_report.xml',
          'wizard/project_from_template.xml',
          'security/ir.model.access.csv'
         ],
 'demo': [],
 'test': [],
 'installable': True,
 'images' : [],
 'auto_install': False,
 'license': 'AGPL-3',
 'application': True,
}
 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
