"""Module with resource classes for department"""
from flask_restful import Resource, marshal_with, fields
from flask import request
from flask_api import status

from models import Department, Employee
from rest.base_api import BaseAPI

_DEPARTMENT_FIELDS = {
    'department_id': fields.Integer,
    'name': fields.String
}


class DepartmentListAPI(Resource, BaseAPI):
    """Resource, BaseAPI class for getting department list"""

    @BaseAPI.handle_error
    @marshal_with(_DEPARTMENT_FIELDS)
    def get(self):
        """Return all departments"""
        departments = self.database.get(Department)
        return departments

    @BaseAPI.handle_error
    def post(self):
        """Create new department"""
        department = Department(**request.form)
        self.database.insert(department)
        return {'success': True}


class DepartmentAPI(Resource, BaseAPI):
    """Resource, BaseAPI class to work with single department"""

    @BaseAPI.handle_error
    @marshal_with(_DEPARTMENT_FIELDS)
    def get(self, department_id):
        """Return department """
        criterion = Department.department_id == department_id
        department = self.database.get_one(cls=Department,
                                           criterion=criterion)
        if department:
            return department
        return {'success': False}, status.HTTP_404_NOT_FOUND

    @BaseAPI.handle_error
    def put(self, department_id):
        """Update department"""
        criterion = Department.department_id == department_id
        self.database.update(Department, criterion, **request.form)
        return {'success': True}

    @BaseAPI.handle_error
    def delete(self, department_id):
        """Update department"""
        criterion = Department.department_id == department_id
        self.database.delete(Department, criterion)
        return {'success': True}


class DepartmentInfoAPI(Resource, BaseAPI):
    """Resource, BaseAPI class to get average salary and number of workers"""

    @BaseAPI.handle_error
    def get(self, department_id):
        """Get detailed department info"""
        criterion = Department.department_id == department_id
        department = self.database.get_one(cls=Department,
                                           criterion=criterion)
        if not department:
            return {'success': False}, status.HTTP_404_NOT_FOUND

        employees = self.database.get(Employee,
                                      Employee.department_id == department_id)
        employees_count = 0
        average_salary = 0
        if employees:
            employees_count = len(employees)
            salaries = [employee.salary for employee in employees]
            average_salary = sum(salaries) / employees_count
        return {'employees_count': employees_count,
                'average_salary': average_salary}
