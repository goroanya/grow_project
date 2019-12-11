"""Module with resource classes for department"""
from flask_restful import Resource, marshal_with, fields
from flask import request

from models import Employee
from rest.base_api import BaseAPI

_EMPLOYEE_FIELDS = {
    'employee_id': fields.Integer,
    'name': fields.String,
    'date_of_birth': fields.String,
    'salary': fields.Integer,
    'department_id': fields.Integer
}


class EmployeeListBaseAPI(Resource, BaseAPI):
    """Resource class for getting department list"""

    @BaseAPI._handle_error
    @marshal_with(_EMPLOYEE_FIELDS)
    def get(self):
        """Return all departments"""
        employees = self._database.get(Employee)
        return employees

    @BaseAPI._handle_error
    def post(self):
        """Create new employee"""
        employee = Employee(**request.form)
        self._database.insert(employee)
        return None, 200


class EmployeeBaseAPI(Resource, BaseAPI):
    """Resource class to work with single employee"""

    @BaseAPI._handle_error
    @marshal_with(_EMPLOYEE_FIELDS)
    def get(self, employee_id):
        """Return employee"""
        criterion = Employee.employee_id == employee_id
        employee = self._database.get_one(cls=Employee,
                                          criterion=criterion)
        return employee

    @BaseAPI._handle_error
    def put(self, employee_id):
        """Update employee"""
        criterion = Employee.employee_id == employee_id
        self._database.update(Employee, criterion, **request.form)
        return None, 200

    @BaseAPI._handle_error
    def delete(self, employee_id):
        """Update employee"""
        criterion = Employee.employee_id == employee_id
        self._database.delete(Employee, criterion)
        return None, 200
