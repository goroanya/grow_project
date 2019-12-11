"""Module with resource classes for department"""
from flask_restful import Resource, marshal_with, fields
from flask import request

from models import Department
from rest.base_api import BaseAPI

_DEPARTMENT_FIELDS = {
    'department_id': fields.Integer,
    'name': fields.String
}


class DepartmentListBaseAPI(Resource, BaseAPI):
    """Resource class for getting department list"""

    @BaseAPI._handle_error
    @marshal_with(_DEPARTMENT_FIELDS)
    def get(self):
        """Return all departments"""
        departments = self._database.get(Department)
        return departments

    @BaseAPI._handle_error
    def post(self):
        """Create new department"""
        department = Department(**request.form)
        self._database.insert(department)
        return None, 200


class DepartmentBaseAPI(Resource, BaseAPI):
    """Resource class to work with single department"""

    @BaseAPI._handle_error
    @marshal_with(_DEPARTMENT_FIELDS)
    def get(self, department_id):
        """Return department """
        criterion = Department.department_id == department_id
        department = self._database.get_one(cls=Department,
                                            criterion=criterion)
        return department

    @BaseAPI._handle_error
    def put(self, department_id):
        """Update department"""
        criterion = Department.department_id == department_id
        self._database.update(Department, criterion, **request.form)
        return None, 200

    @BaseAPI._handle_error
    def delete(self, department_id):
        """Update department"""
        criterion = Department.department_id == department_id
        self._database.delete(Department, criterion)
        return None, 200
