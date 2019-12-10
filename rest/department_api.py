"""Module with resource classes for department"""
from flask_restful import Resource

from models import Department
from rest.api import API


class DepartmentListAPI(Resource, API):
    """Resource class gor getting department list"""
    def get(self):
        """Return all departments"""
        departments = self.database.get(Department)
        return Department.serialize_list(departments)
