"""Module with resource classes for employees"""
from sqlalchemy import and_
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

    @BaseAPI.handle_error
    @marshal_with(_EMPLOYEE_FIELDS)
    def get(self):
        """Return all employees
        @return: list of all employees in json
        """
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        criterion = None
        if start_date and end_date:
            start_date = Employee.date_from_str(start_date)
            end_date = Employee.date_from_str(end_date)
            criterion = and_(Employee.date_of_birth >= start_date,
                             Employee.date_of_birth <= end_date)
        employees = self.database.get(Employee, criterion)
        return employees

    @BaseAPI.handle_error
    def post(self):
        """Create new employee
        @return: result and new employee's id
        """
        employee = self.database.insert(Employee(**request.form))
        return {'success': True, 'employee_id': employee.employee_id}


class EmployeeAPI(Resource, BaseAPI):
    """Resource class to work with single employee"""

    @BaseAPI.handle_error
    @marshal_with(_EMPLOYEE_FIELDS)
    def get(self, employee_id):
        """Return employee
        @param employee_id: unique employee's id
        @return: result
        """
        criterion = Employee.employee_id == employee_id
        employee = self.database.get_one(cls=Employee,
                                         criterion=criterion)
        if employee:
            return employee
        return {'success': False}, status.HTTP_404_NOT_FOUND

    @BaseAPI.handle_error
    def put(self, employee_id):
        """Update employee
        @param employee_id: unique employee's id
        @return: result
        """
        criterion = Employee.employee_id == employee_id
        self.database.update(Employee, criterion, **request.form)
        return {'success': True}

    @BaseAPI.handle_error
    def delete(self, employee_id):
        """Delete employee
        @param employee_id: unique employee's id
        @return: result
        """
        criterion = Employee.employee_id == employee_id
        self.database.delete(Employee, criterion)
        return {'success': True}
