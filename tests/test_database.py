"""Module to test CRUD operations with DB using DataBase class"""
import unittest
from datetime import date

from service import DataBase
from models import Employee, Department

DEPARTMENTS = [
    Department('First Department'),
    Department('Second Department'),
]

EMPLOYEES = [
    Employee('First Employee', date(2000, 1, 1), 100, 1),
    Employee('Second Employee', date(2001, 1, 1), 200, 1),
    Employee('Third Employee', date(2002, 1, 1), 300, 1),
    Employee('Fourth Employee', date(2002, 2, 1), 400, 1),
    Employee('Fifth Employee', date(2003, 1, 1), 500, 2),
    Employee('Sixth Employee', date(2004, 1, 1), 600, 2),
]


class TestDataBase(unittest.TestCase):
    """Test case class to test all operations"""

    @classmethod
    def setUpClass(cls):
        cls.database = DataBase('sqlite:///')
        for department in DEPARTMENTS:
            cls.database.insert(department)
        for employee in EMPLOYEES:
            cls.database.insert(employee)

    def test_simple_get(self):
        """Test case to check getting all entities from DB"""
        employees = self.database.get(Employee)
        self.assertEqual(employees, EMPLOYEES)

        departments = self.database.get(Department)
        self.assertEqual(departments, DEPARTMENTS)

    def test_filtered_get(self):
        """Test case to check getting entities from DB with filters"""
        from_database = self.database.get(Employee, False)
        self.assertEqual(from_database, [])

        from_database = self.database.get(Employee, Employee.employee_id > 3)
        expected = [employee for employee in EMPLOYEES
                    if employee.employee_id > 3]
        self.assertEqual(from_database, expected)

        tmp_date = date(2005, 5, 5)
        from_database = self.database.get(Employee,
                                          Employee.date_of_birth < tmp_date)
        expected = [employee for employee in EMPLOYEES
                    if employee.date_of_birth < tmp_date]
        self.assertEqual(from_database, expected)

        from_database = self.database.get(Department, True)
        self.assertEqual(from_database, DEPARTMENTS)

        from_database = self.database.get(Department,
                                          Department.name > 'foobar')
        expected = [department for department in DEPARTMENTS
                    if department.name > 'foobar']
        self.assertEqual(from_database, expected)

    def test_get_with_limit_and_offset(self):
        """Test to check if limit and offset parameters are working"""
        from_database = self.database.get(Employee, limit=0)
        self.assertEqual(from_database, [])

        from_database = self.database.get(Employee, limit=2)
        self.assertEqual(from_database, EMPLOYEES[:2])

        from_database = self.database.get(Employee, limit=1000)
        self.assertEqual(from_database, EMPLOYEES)

        from_database = self.database.get(Employee, offset=0)
        self.assertEqual(from_database, EMPLOYEES)

        from_database = self.database.get(Employee, offset=5)
        self.assertEqual(from_database, EMPLOYEES[5:])

        from_database = self.database.get(Employee, offset=1000)
        self.assertEqual(from_database, [])

        from_database = self.database.get(Employee, limit=2, offset=3)
        self.assertEqual(from_database, EMPLOYEES[3:5])

    def test_get_one(self):
        """Testing getting only one entity from DB"""
        criterion = Employee.employee_id == 3
        from_database = self.database.get_one(cls=Employee, criterion=criterion)
        self.assertEqual(from_database, EMPLOYEES[2])

        from_database = self.database.get_one(cls=Employee, criterion=False)
        self.assertIsNone(from_database)

    def test_simple_insert_and_delete(self):
        """Test for inserting and deleting both employee and department"""
        new_employee = Employee('new employee', date(2000, 1, 1), 150, 1)
        employee_criretion = Employee.name == 'new employee'
        inserted_employee = self.database.insert(new_employee)
        self.assertIsNotNone(inserted_employee.employee_id)
        from_database = self.database.get_one(cls=Employee,
                                              criterion=employee_criretion)
        self.assertEqual(new_employee, from_database)

        self.database.delete(cls=Employee, criterion=employee_criretion)
        from_database = self.database.get_one(cls=Employee,
                                              criterion=employee_criretion)
        self.assertIsNone(from_database)

        new_department = Department('new department')
        department_criterion = Department.name == 'new department'
        inserted_department = self.database.insert(new_department)
        self.assertIsNotNone(inserted_department.department_id)
        from_database = self.database.get_one(cls=Department,
                                              criterion=department_criterion)
        self.assertEqual(new_department, from_database)

        self.database.delete(cls=Department, criterion=department_criterion)
        from_database = self.database.get_one(cls=Department,
                                              criterion=department_criterion)
        self.assertIsNone(from_database)

    def test_update(self):
        """Test for updating entities in DB"""
        employee = EMPLOYEES[0]
        new_name = 'new name'
        old_name = employee.name

        id_criterion = Employee.employee_id == employee.employee_id
        self.database.update(Employee, id_criterion, name=new_name,
                             date_of_birth='2010-5-24')
        updated = self.database.get_one(cls=Employee, criterion=id_criterion)
        self.assertEqual(updated.name, new_name)
        self.assertEqual(updated.date_of_birth, date(2010, 5, 24))

        self.database.update(Employee, id_criterion, name=old_name)
        updated = self.database.get_one(cls=Employee, criterion=id_criterion)
        self.assertEqual(updated.name, old_name)
