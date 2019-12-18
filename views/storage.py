"""Module to work with REST server API"""
import os

import requests
from flask_api import status
from dotenv import load_dotenv
from flask.testing import FlaskClient

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

load_dotenv()
SERVER_URL = os.getenv('SERVER_URL')
if not SERVER_URL:
    SERVER_URL = ''
    from rest import APP
    from service import DataBase
    APP.config['DATABASE'] = DataBase('sqlite:///')
    requests = APP.test_client()


class RequestException(Exception):
    """Default exception to raise when request failed"""
    def __init__(self, error_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code


def __requests(func, url, *args, **kwargs):
    response = func(f'{SERVER_URL}{url}', *args, **kwargs)
    if response.status_code != status.HTTP_200_OK:
        raise RequestException(error_code=response.status_code)
    if isinstance(requests, FlaskClient):
        return response.json
    return response.json()


def get_employees(start_date=None, end_date=None):
    """
    @param start_date: lower bound for date of birth
    @param end_date: upper bound for date of birth
    @return: list of employees
    """
    request_str = f'/employees'
    if start_date and end_date:
        request_str = f'{request_str}?start_date={start_date}&end_date={end_date}'
    employees = __requests(requests.get, request_str)
    for employee in employees:
        department = get_department(employee['department_id'])
        employee['department_name'] = department['name']
    return sorted(employees, key=lambda x: x['employee_id'])


def get_employee(employee_id):
    """
    @param employee_id: unique employee's id
    @return: employee by given id
    """
    employee = __requests(requests.get, f'/employees/{employee_id}')
    department = get_department(employee['department_id'])
    employee['department_name'] = department['name']

    employee['user_pic'] = '/static/images/userpic.jpg'
    path = f'static/images/employees/{employee["employee_id"]}.png'
    if os.path.exists(path):
        employee['user_pic'] = f'/{path}'

    return employee


def get_departments():
    """
    @return: list off all departments
    """
    departments = __requests(requests.get, f'/departments')
    for department in departments:
        info = __get_department_info(department['department_id'])
        department.update(info)
    return sorted(departments, key=lambda x: x['department_id'])


def __get_department_info(department_id):
    info = __requests(requests.get,
                      f'/departments/info/{department_id}')
    return info


def get_department(department_id):
    """
    @param department_id: unique department's id
    @return: department by given id
    """
    department = __requests(requests.get,
                            f'/departments/{department_id}')
    info = __get_department_info(department['department_id'])
    department.update(info)
    return department


def delete_employee(employee_id):
    """Delete employee by given id
    @param employee_id: unique employee's id
    """
    __requests(requests.delete, f'/employees/{employee_id}')


def delete_department(department_id):
    """Delete department by given id
    @param department_id: unique department's id
    """
    __requests(requests.delete, f'/departments/{department_id}')


def insert_employee(form):
    """Insert new employee
    @param form: new values dictionary
    @return: new employee's id
    """
    response = __requests(requests.post, f'/employees', data=form)
    return response['employee_id']


def edit_employee(employee_id, form):
    """Edit employee
    @param employee_id: unique employee's id
    @param form: new values dictionary
    """
    __requests(requests.put, f'/employees/{employee_id}', data=form)


def insert_department(form):
    """Insert new department
    @param form: new values dictionary
    @return: new department's id
    """
    response = __requests(requests.post, f'/departments', data=form)
    return response['department_id']


def edit_department(department_id, form):
    """Edit department
    @param department_id: unique department's id
    @param form: new values dictionary
    """
    __requests(requests.put, f'/departments/{department_id}', data=form)
