"""Module with department class"""
from sqlalchemy import Column, Integer, String, Date, ForeignKey

from models.base import BaseClass


class Employee(BaseClass):
    """Employee class to work with DB using ORM"""
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String, default='anonymous')
    date_of_birth = Column(Date, nullable=False)
    salary = Column(Integer, default=0)
    department_id = Column(Integer, ForeignKey('department.department_id'),
                           nullable=False)

    def __init__(self, name, date_of_birth, salary, department_id):
        self.name = name
        self.date_of_birth = date_of_birth
        self.salary = salary
        self.department_id = department_id

    def serialize(self):
        """Return employee data in easily serializable format"""
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'date_of_birth': str(self.date_of_birth),
            'salary': self.salary,
            'department_id': self.department_id
        }

    @staticmethod
    def serialize_list(departments):
        """Return list of serialized employees"""
        return [department.serialize() for department in departments]