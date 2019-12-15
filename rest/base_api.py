"""Module for base resource class"""
from flask_api import status

from rest.app import APP


class BaseAPI:
    """Base resource class"""
    @property
    def database(self):
        """Return DB instance
        @return: current DB instance for REST flask app
        """
        return APP.config['DATABASE']

    @staticmethod
    def handle_error(func):
        """Decorator for handling errors
        @param func: function to execute
        @return: result of calling given function
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError as exception:
                return {'error': str(exception)}, status.HTTP_400_BAD_REQUEST
            except Exception as exception:
                return {'error': str(exception)}, \
                       status.HTTP_500_INTERNAL_SERVER_ERROR
        return wrapper
