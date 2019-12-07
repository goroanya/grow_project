# Python Autumn 2019 Graduation Work

**Table of Contents**
* [Description](#description)
  * [Technical requirements:](#technical-requirements)
  * [The web application should allow:](#the-web-application-should-allow)
* [Employees](#employees)
  * [List all employees](#list-all-employees)
  * [Add employee](#add-employee)
  * [Edit employee](#edit-employee)
  * [Removing the employee](#removing-the-employee)
* [Departments](#departments)
  * [List all departments](#list-all-departments)
  * [Add department](#add-department)
  * [Edit department](#edit-department)
  * [Removing the department](#removing-the-department)

## Description
This is a simple web application for managing departments and employees.
### Technical requirements:
- Storing data and reading from database;
- Ability to deploy the web application on Gunicorn using command line;
- All public functions / methods on all levels should include unit tests;
- Debug information should be displayed at the debugging level in the console and in a separate file;
- Classes and functions / methods must have docstrings comments;
- Final `README.md` should contain a brief description of the project, instructions on how to build a project from the command line, how to start it, and at what addresses the Web service and the Web application will be available after launch.
### The web application should allow:
- Display a list of departments and the average salary (calculated automatically) for these departments;
- Display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates;
- Change (add / edit / delete) the above data.

## Employees
### List all employees
Mode is designed to view list of all employees, search employees by born date and paginate list.
![all_employees](https://drive.google.com/uc?export=view&id=1tJka_p_0PMp_DaFAQIjG36uBnj7Kh1J2)

*Pic 1.1. List of all employees*

__*Main scenario:*__
- User press link `Employees` at the navigation bar;
- List of all employees is displayed for user.

__*List displays the following columns:*__
- _Name_ - full name of an employee;
- _Department_ - name of department the employee is working at;
- _Salary_ - employee's salary in $;
- _Born date_ - employee's born date in format dd/mm/yyyy.

### Add employee
![add_employee](https://drive.google.com/uc?export=view&id=1zni99aLLjo3C-HymSuF2llagDQ2QSql2)

*Pic 1.2. Add employee form*

__*Main scenario:*__
- User clicks the `+` button in the employees list view mode;
- Application displays form to enter employee data;
- User enters employee data and presses `Create` button;
- If any data is entered incorrectly, incorrect data messages are displayed;
- If entered data is valid, then record is adding to database;
- If error occurs, then error message is displaying;
- If new employee record is successfully added, then list of employees with added records is displaying.

__*Cancel operation scenario:*__
- User clicks the `+` button in the employees list view mode;
- Application displays form to enter employee data;
- If user does not press `Create` button no employee will be added to database.

__*When adding an employee, the following details are entered:*__
- Employee name – employee’s first and last name;
- Department name – department's name (choosing from dropdown list with existing departments);
- Salary – employee's salary in $;
- Born date – date when an employee was born.

### Edit employee
![edit_employee](https://drive.google.com/uc?export=view&id=1ppUODQjlDRNLkDmC3kJsoYar_V98gOWP)

*Pic 1.3. Edit employee form*

__*Main scenario:*__
- User clicks on the employee's name in the employees list view mode;
- On the employee's page user click button `Edit';
- Application displays form to enter new employee data with default values from old employee data;
- User change data and presses `Save` button;
- If any data is entered incorrectly, incorrect data messages are displayed;
- If entered data is valid, then employee is edited in database;
- If error occurs, then error message is displaying;
- If employee record is successfully edited, then list of employees with added records is displaying.

__*Cancel operation scenario:*__
- User clicks on the employee's name in the employees list view mode;
- Application displays form to enter new employee data with default values from old employee's data;
- If user does not press `Create` button no employee will be edited in database.

__*When editing an employee, the following details are entered:*__
- Employee name – employee’s first and last name;
- Department name – department's name (choosing from dropdown list with existing departments);
- Salary – employee's salary in $;
- Born date – date when an employee was born.

__*Constraints for data validation:*__
- Employee name – first and last name divided with space, contains only latin letters, maximum length is 30 characters.
- Salary – number from 0 to 5000;
- Born date – date in format dd/mm/yyyy.

### Removing the employee
![delete_employee](https://drive.google.com/uc?export=view&id=17wLX3dfICPDP7GdS9I1wpKSTgGiC9ei9)

*Pic 1.4. Delete employee confirmation dialog*

__*Main scenario:*__
- The user, while in the list of employees, presses the `Delete` button in the selected order line;
- Confirmation dialog is displayed;
- The user confirms the removal of the employee by pressing `Yes, delete` button;
- Record is deleted from database;
- If error occurs, then error message displays;
- If employee record is successfully deleted, then list of employees without deleted records is displaying.

__*Cancel operation scenario:*__
- The user, while in the list of employees, presses the `Delete` button in the selected order line;
- Confirmation dialog is displayed;
- The user cancels the removal of the employee by pressing `Cancel` button;

## Departments
### List all departments
Mode is designed to view list of all departments with automatically calculated average salary value.
![all_departments](https://drive.google.com/uc?export=view&id=1DHsjmsWujuvCYjm9V1YP7DiOvSoqBX5Z)

*Pic 2.1. List of all departments*

__*Main scenario:*__
- User press link `Departments` at the navigation bar;
- List of all departments is displayed for user.

__*List displays the following columns:*__
- _Name_ - name of department;
- _Average salary_ - calculated average salary for this department.

### Add department
![add_department](https://drive.google.com/uc?export=view&id=1WZ3D9kKHkmvDivrT7Ds7onYeomfwEzHM)

*Pic 2.2. Add department form*

__*Main scenario:*__
- User clicks the `+` button in the departments list view mode;
- Application displays form to enter department data;
- User enters department data and presses `Create` button;
- If any data is entered incorrectly, incorrect data messages are displayed;
- If entered data is valid, then record is adding to database;
- If error occurs, then error message is displaying;
- If new department record is successfully added, then list of departments with added records is displaying.

__*Cancel operation scenario:*__
- User clicks the `+` button in the departments list view mode;
- Application displays form to enter department data;
- If user does not press `Create` button no department will be added to database.

__*When adding an department, the following details are entered:*__
- Department name – department’s name.

### Edit department
![edit_department](https://drive.google.com/uc?export=view&id=1e2EPTodaCAWgVzZcnBXKGX84W6qi_icz)

*Pic 2.3. Edit department form*

__*Main scenario:*__
- User clicks on the department's name in the departments list view mode;
- On the department's page user click button `Edit`;
- Application displays form to enter new department data with default values from old department's data;
- User change data and presses `Save` button;
- If any data is entered incorrectly, incorrect data messages are displayed;
- If entered data is valid, then department is edited in database;
- If error occurs, then error message is displaying;
- If department record is successfully edited, then list of departments with added records is displaying.

__*Cancel operation scenario:*__
- User clicks on the department's name in the departments list view mode;
- Application displays form to enter new department data with default values from old department data;
- If user does not press `Create` button no employee will be edited in database.

__*When editing an department, the following details are entered:*__
- Department name – department’s name.

__*Constraints for data validation:*__
- Department name – contains only latin letters, maximum length is 30 characters.


### Removing the department
![delete_department](https://drive.google.com/uc?export=view&id=1KzSHc-PDlLm2pOXm2plLmdIR3CK_WyOF)

*Pic 2.4. Delete department confirmation dialog*

__*Main scenario:*__
- The user, while in the list of departments, presses the `Delete` button in the selected order line;
- Confirmation dialog is displayed;
- The user confirms the removal of the department by pressing `Yes, delete` button;
- Record is deleted from database;
- If error occurs, then error message displays;
- If department record is successfully deleted, then list of departments without deleted records is displaying.

__*Cancel operation scenario:*__
- The user, while in the list of departments, presses the `Delete` button in the selected order line;
- Confirmation dialog is displayed;
- The user cancels the removal of the department by pressing `Cancel` button;
