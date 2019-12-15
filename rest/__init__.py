"""This package includes modules with RESTful service implementation"""
from flask_restful import Api

from rest.department_api import *
from rest.employee_api import *
from rest.app import APP

API = Api(APP)
API.add_resource(DepartmentListAPI, '/departments')
API.add_resource(DepartmentInfoAPI, '/departments/info/<int:department_id>')
API.add_resource(DepartmentAPI, '/departments/<int:department_id>')
API.add_resource(EmployeeListAPI, '/employees')
API.add_resource(EmployeeAPI, '/employees/<int:employee_id>')
