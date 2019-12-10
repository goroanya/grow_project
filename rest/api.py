"""Module with default APi resources base class"""
import os

from service import DataBaseFactory


class API:
    """Default APi resources base class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        database_url = os.getenv('DATABASE_URL')
        self.database = DataBaseFactory.get_database(database_url)
