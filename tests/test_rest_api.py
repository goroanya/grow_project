"""Module for testing REST api server"""
import unittest

from flask_api import status

from rest import APP
from service import DataBase


class TestRestApi(unittest.TestCase):
    """Test case class to test REST API server"""

    @classmethod
    def setUpClass(cls):
        APP.config['TESTING'] = True
        APP.config['WTF_CSRF_ENABLED'] = False
        APP.config['DEBUG'] = False
        APP.config['DATABASE'] = DataBase('sqlite:///')

        cls.app = APP.test_client()

    def test_get_empty(self):
        """Test getting entities while DB is empty"""
        response = self.app.get('/departments')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, [])

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, [])

    def test_post_invalid_args(self):
        """Test post with invalid arguments"""
        response = self.app.post('/departments', data={'foo': 'bar'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.app.post('/employees', data={'foo': 'bar'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.app.post('/employees', data={'name': 'foobar'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_departments(self):
        """Test all operation with departments"""
        response = self.app.post('/departments', data={'name': 'foobar'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/departments')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json,
                         [{'department_id': 1, 'name': 'foobar'}])

        response = self.app.put('/departments/1', data={'name': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, {'department_id': 1, 'name': 'foo'})

        response = self.app.delete('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_all_employees(self):
        """Test all operation with employees"""
        response = self.app.post('/departments', data={'name': 'foobar'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        employee_data = {
            'name': 'foobar',
            'date_of_birth': '2000-01-01',
            'salary': 150,
            'department_id': 1
        }
        response = self.app.post('/employees', data=employee_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        employee_data['employee_id'] = 1
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, [employee_data])

        response = self.app.put('/employees/1', data={'name': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        employee_data['name'] = 'foo'
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json, employee_data)

        response = self.app.delete('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.app.delete('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
