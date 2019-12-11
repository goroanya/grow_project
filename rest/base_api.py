"""Module with default APi resources base class"""
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
            print(args, kwargs)
            try:
                return func(*args, **kwargs)
            # pylint: disable=broad-except
            except Exception as exception:
                return {'error': str(exception)}, 500
        return wrapper
