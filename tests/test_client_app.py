"""Module for testing client WEB app"""
import unittest

from flask_api import status

from views import APP as app


class TestClientApp(unittest.TestCase):
    """Test case class to test REST API server"""

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        cls.app = app.test_client()

    def test_get_index_page(self):
        """Test redirecting from index page"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_empty_list(self):
        """Test getting entities while DB is empty"""
        response = self.app.get('/departments')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_entity(self):
        """Test case for getting entity page"""
        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        """Test delete operation with entities"""
        response = self.app.post('/departments/delete/1')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self.app.post('/employees/delete/1')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_add_page(self):
        """Test get new entity page"""
        response = self.app.get('/departments/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/employees/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_entity_invalid_form(self):
        """Testing adding new entities with invalid form"""
        response = self.app.post('/departments/new')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.app.post('/employees/new')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_entity_valid_form(self):
        """Testing adding new entities with valid form"""
        response = self.app.post('/departments/new', data={'name': 'foo'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_employee = {'name': 'foo', 'date_of_birth': '2010-01-01',
                        'salary': 100, 'department_id': 1}
        response = self.app.post('/employees/new', data=new_employee)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.post('/employees/delete/1')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.post('/departments/delete/1')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.app.get('/departments/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_page_invalid_index(self):
        """Test get edit entity page with invalid index"""
        response = self.app.get('/departments/edit/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.app.get('/employees/edit/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_page(self):
        """Test editing entities"""
        self.app.post('/departments/new', data={'name': 'foo'})
        response = self.app.get('/departments/edit/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.post('/departments/edit/1', data={'name': 'bar'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        new_employee = {'name': 'foo', 'date_of_birth': '2010-01-01',
                        'salary': 100, 'department_id': 1}
        response = self.app.post('/employees/new', data=new_employee)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.app.post('/employees/edit/1', data={'name': 'bar'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.app.post('/employees/delete/1')
        self.app.post('/departments/delete/1')
