"""This package includes modules with RESTful service implementation"""
from flask_restful import Resource, Api
from flask import Flask

from rest.department_api import DepartmentListAPI
from rest.employee_api import EmployeeListAPI

APP = Flask(__name__)
API = Api(APP)
API.add_resource(DepartmentListAPI, '/departments')
API.add_resource(EmployeeListAPI, '/employees')
