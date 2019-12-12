"""Module with default APi resources base class"""
from flask_api import status

from rest.app import APP


class BaseAPI:
    """Default APi resources base class"""
    @property
    def _database(self):
        return APP.config['DATABASE']

    @staticmethod
    def _handle_error(func):
        """Decorator for handling errors"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError as exception:
                return {'error': str(exception)}, status.HTTP_400_BAD_REQUEST
            except Exception as exception:
                return {'error': str(exception)},\
                       status.HTTP_500_INTERNAL_SERVER_ERROR
        return wrapper
