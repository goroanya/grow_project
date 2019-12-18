"""Module to initialize client web app"""
import os
import functools
import http.client

from flask import Flask, render_template, redirect, request
from flask_api import status

import views.storage as storage

APP = Flask(__name__, template_folder='../templates')


def __error_handler(func):
    """Decorator to handle internal and external errors"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except storage.RequestException as exception:
            code = exception.error_code
            message = http.client.responses[code]
            return render_template('error.html',
                                   error=f'{code}: {message}',
                                   title='ERROR'), code
        except Exception as error:
            return render_template('error.html',
                                   error=f'500: {error}',
                                   title='ERROR'), \
                   status.HTTP_500_INTERNAL_SERVER_ERROR

    return wrapper


@APP.route('/')
def index():
    """
    @return: redirect to employees list mode
    """
    return redirect('/employees')


@APP.route('/employees', methods=['GET'])
@__error_handler
def get_employees():
    """
    @return: page with employees list mode
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    employees = storage.get_employees(start_date, end_date)
    return render_template('employees.html',
                           title='Employees',
                           employees=employees,
                           start_date=start_date,
                           end_date=end_date)


@APP.route('/employees/<int:employee_id>', methods=['GET'])
@__error_handler
def get_employee(employee_id):
    """
    @param employee_id: unique employee's id
    @return: page with employee's info
    """
    employee = storage.get_employee(employee_id)
    return render_template('employee.html',
                           title=employee['name'],
                           **employee)


@APP.route('/departments', methods=['GET'])
@__error_handler
def get_departments():
    """
    @return: page with departments list mode
    """
    departments = storage.get_departments()
    return render_template('departments.html',
                           title='Departments',
                           departments=departments)


@APP.route('/departments/<int:department_id>', methods=['GET'])
@__error_handler
def get_department(department_id):
    """
    @param department_id: unique departments's id
    @return: page with department info
    """
    department = storage.get_department(department_id)
    return render_template('department.html',
                           title=department['name'],
                           **department)


@APP.route('/employees/delete/<int:employee_id>', methods=['POST'])
@__error_handler
def delete_employee(employee_id):
    """
    @param employee_id: unique employee's id
    @return: redirect to employees list mode
    """
    storage.delete_employee(employee_id)
    return redirect('/employees')


@APP.route('/departments/delete/<int:department_id>', methods=['POST'])
@__error_handler
def delete_department(department_id):
    """
    @param department_id: unique department's id
    @return: redirect to departments list mode
    """
    storage.delete_department(department_id)
    return redirect('/departments')


@APP.route('/employees/new', methods=['GET'])
@__error_handler
def add_employee_page():
    """
    @return: page with form to create new employee
    """
    departments = storage.get_departments()
    return render_template('employee_new.html',
                           title='New employee',
                           departments=departments)


def _save_user_pic(employee_id, file):
    filename = file.filename
    extension = filename.lower().split('.')[-1]
    if extension not in storage.ALLOWED_EXTENSIONS:
        raise storage.RequestException(status.HTTP_400_BAD_REQUEST)
    file.save(os.path.join('static/images/employees/', f'{employee_id}.{extension}'))


@APP.route('/employees/new', methods=['POST'])
@__error_handler
def add_employee():
    """
    @return: redirect to created employee's page
    """
    employee_id = storage.insert_employee(request.form)
    if 'user_pic' in request.files and request.files['user_pic']:
        _save_user_pic(employee_id, request.files['user_pic'])
    return redirect(f'/employees/{employee_id}')


@APP.route('/employees/edit/<int:employee_id>', methods=['GET'])
@__error_handler
def edit_employee_page(employee_id):
    """
    @param employee_id: unique employee's id
    @return: page with for to edit employee
    """
    departments = storage.get_departments()
    employee = storage.get_employee(employee_id)
    return render_template('employee_edit.html',
                           title='Edit employee',
                           departments=departments,
                           employee=employee)


@APP.route('/employees/edit/<int:employee_id>', methods=['POST'])
@__error_handler
def edit_employee(employee_id):
    """
    @param employee_id: unique employee's id
    @return: redirect to edited employee's page
    """
    storage.edit_employee(employee_id, request.form)
    if 'user_pic' in request.files and request.files['user_pic']:
        _save_user_pic(employee_id, request.files['user_pic'])
    return redirect(f'/employees/{employee_id}')


@APP.route('/departments/new', methods=['GET'])
@__error_handler
def add_department_page():
    """
    @return: page with form to create new department
    """
    return render_template('department_new.html',
                           title='New department')


@APP.route('/departments/new', methods=['POST'])
@__error_handler
def add_department():
    """
    @return: redirect to new department's page
    """
    department_id = storage.insert_department(request.form)
    return redirect(f'/departments/{department_id}')


@APP.route('/departments/edit/<int:department_id>', methods=['GET'])
@__error_handler
def edit_department_page(department_id):
    """
    @param department_id: unique department's id
    @return: page with form to edit department
    """
    department = storage.get_department(department_id)
    return render_template('department_edit.html',
                           title='Edit department',
                           department=department)


@APP.route('/departments/edit/<int:department_id>', methods=['POST'])
@__error_handler
def edit_department(department_id):
    """
    @param department_id: unique department's id
    @return: redirect to edited department's page
    """
    storage.edit_department(department_id, request.form)
    return redirect(f'/departments/{department_id}')
