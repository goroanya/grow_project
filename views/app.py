"""Module to initialize client web app"""
import functools
import http.client

from flask import Flask, render_template, redirect
from flask_api import status

import views.communicate as requests

APP = Flask(__name__, template_folder='../templates')


def __error_handler(func):
    """Decorator to handle internal and external errors"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as exception:
            code = exception.error_code
            message = http.client.responses[code]
            return render_template('error.html',
                                   error=f'{code}: {message}',
                                   title='ERROR'), code
        except Exception as error:
            return render_template('error.html',
                                   error=f'500: {error}',
                                   title='ERROR'),\
                   status.HTTP_500_INTERNAL_SERVER_ERROR
    return wrapper


@APP.route('/')
def index():
    """Return start page"""
    return redirect('/employees')


@APP.route('/employees', methods=['GET'])
@__error_handler
def get_employees():
    """Return page with employees list"""
    employees = requests.get_employees()
    return render_template('employees.html',
                           title='Employees',
                           employees=employees)


@APP.route('/employees/<int:employee_id>', methods=['GET'])
@__error_handler
def get_employee(employee_id):
    """Return page with employee by given id"""
    employee = requests.get_employee(employee_id)
    return render_template('employee.html',
                           title=employee['name'],
                           **employee)


@APP.route('/departments', methods=['GET'])
@__error_handler
def get_departments():
    """Return page with departments list"""
    departments = requests.get_departments()
    return render_template('departments.html',
                           title='Departments',
                           departments=departments)


@APP.route('/departments/<int:department_id>', methods=['GET'])
@__error_handler
def get_department(department_id):
    """Return page with employee by given id"""
    department = requests.get_department(department_id)
    return render_template('department.html',
                           title=department['name'],
                           **department)


@APP.route('/employees/delete/<int:employee_id>', methods=['POST'])
@__error_handler
def delete_employee(employee_id):
    """Delete request handler for employee"""
    requests.delete_employee(employee_id)
    return redirect('/employees')


@APP.route('/departments/delete/<int:department_id>', methods=['POST'])
@__error_handler
def delete_department(department_id):
    """Delete request handler for employee"""
    requests.delete_department(department_id)
    return redirect('/departments')
