"""Module to work with REST server API"""
import os

import requests
from flask_api import status
from dotenv import load_dotenv

load_dotenv()
SERVER_URL = os.getenv('SERVER_URL') or 'http://server.test'


class RequestException(Exception):
    """Default exception to raise when request failed"""
    def __init__(self, error_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code


def __requests(func, *args, **kwargs):
    response = func(*args, **kwargs)
    if response.status_code != status.HTTP_200_OK:
        raise RequestException(error_code=response.status_code)
    return response.json()


def get_employees():
    """Return all employees"""
    employees = __requests(requests.get, f'{SERVER_URL}/employees')
    for employee in employees:
        department = get_department(employee['department_id'])
        employee['department_name'] = department['name']
    return employees


def get_employee(employee_id):
    """Return employee by given id"""
    employee = __requests(requests.get, f'{SERVER_URL}/employees/{employee_id}')
    department = get_department(employee['department_id'])
    employee['department_name'] = department['name']
    return employee


def get_departments():
    """Return all departments"""
    departments = __requests(requests.get, f'{SERVER_URL}/departments')
    for department in departments:
        info = __get_department_info(department['department_id'])
        department.update(info)
    return departments


def __get_department_info(department_id):
    """Return detailed department info"""
    info = __requests(requests.get,
                      f'{SERVER_URL}/departments/info/{department_id}')
    return info


def get_department(department_id):
    """Return department full info"""
    department = __requests(requests.get,
                            f'{SERVER_URL}/departments/{department_id}')
    info = __get_department_info(department['department_id'])
    department.update(info)
    return department
