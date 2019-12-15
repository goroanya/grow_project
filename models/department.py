"""Module with department class"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import BaseClass


class Department(BaseClass):
    """Department class to work with DB using ORM"""

    __tablename__ = 'department'

    department_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    employees = relationship('Employee')

    def __init__(self, name):
        self.name = name
