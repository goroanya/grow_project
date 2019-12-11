"""This package includes modules with RESTful service implementation"""
from flask_restful import Resource, Api

from rest.department_api import DepartmentListBaseAPI, DepartmentBaseAPI
from rest.employee_api import EmployeeListBaseAPI, EmployeeBaseAPI
from rest.app import APP

API = Api(APP)
API.add_resource(DepartmentListBaseAPI, '/departments')
API.add_resource(DepartmentBaseAPI, '/departments/<int:department_id>')
API.add_resource(EmployeeListBaseAPI, '/employees')
API.add_resource(EmployeeBaseAPI, '/employees/<int:employee_id>')
