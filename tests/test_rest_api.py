"""Module for testing REST api server"""
import unittest

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

    def test_empty(self):
        """Test getting entities wile DB is empty"""
        response = self.app.get('/departments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
