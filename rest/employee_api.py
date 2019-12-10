"""Module with resource classes for department"""
from flask_restful import Resource

from models import Employee
from rest.api import API


class EmployeeListAPI(Resource, API):
    """Resource class gor getting department list"""
    def get(self):
        """Return all departments"""
        employees = self.database.get(Employee)
        return Employee.serialize_list(employees)
