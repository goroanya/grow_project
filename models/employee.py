"""Module with department class"""
import datetime

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
        if isinstance(date_of_birth, datetime.date):
            self.date_of_birth = date_of_birth
        else:
            self.date_of_birth = Employee.date_from_str(date_of_birth)
        self.salary = salary
        self.department_id = department_id

    @staticmethod
    def date_from_str(str_object):
        """Convert string to date"""
        year, month, day = str(str_object).split('-')
        return datetime.date(int(year), int(month), int(day))
