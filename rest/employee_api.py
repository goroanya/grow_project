"""Module with resource classes for department"""
from flask_restful import Resource, marshal_with, fields
from flask import request
from flask_api import status

from models import Employee
from rest.base_api import BaseAPI


_EMPLOYEE_FIELDS = {
    'employee_id': fields.Integer,
    'name': fields.String,
    'date_of_birth': fields.String,
    'salary': fields.Integer,
    'department_id': fields.Integer
}


class EmployeeListAPI(Resource, BaseAPI):
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
        return {'success': True}


class EmployeeAPI(Resource, BaseAPI):
    """Resource class to work with single employee"""

    @BaseAPI._handle_error
    @marshal_with(_EMPLOYEE_FIELDS)
    def get(self, employee_id):
        """Return employee"""
        criterion = Employee.employee_id == employee_id
        employee = self._database.get_one(cls=Employee,
                                          criterion=criterion)
        if employee:
            return employee
        return {'success': False}, status.HTTP_404_NOT_FOUND

    @BaseAPI._handle_error
    def put(self, employee_id):
        """Update employee"""
        criterion = Employee.employee_id == employee_id
        self._database.update(Employee, criterion, **request.form)
        return {'success': True}

    @BaseAPI._handle_error
    def delete(self, employee_id):
        """Update employee"""
        criterion = Employee.employee_id == employee_id
        self._database.delete(Employee, criterion)
        return {'success': True}
