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
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

        response = self.app.get('/employees')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_invalid_index(self):
        """Test get operation with entities"""
        response = self.app.get('/departments/15')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

        response = self.app.get('/employees/15')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_delete(self):
        """Test delete operation with entities"""
        response = self.app.post('/departments/delete/15')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

        response = self.app.post('/employees/delete/15')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_add_page(self):
        """Test get new entity page"""
        response = self.app.get('/departments/new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.app.get('/employees/new')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

    def test_edit_page(self):
        """Test get edit entity page"""
        response = self.app.get('/departments/edit/1')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

        response = self.app.get('/employees/edit/1')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
