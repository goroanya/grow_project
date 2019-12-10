"""Factory DB module"""
from service.database import DataBase


class DataBaseFactory:
    """Class to get DB instance as singleton"""
    __factory = {}

    @staticmethod
    def get_database(database_url):
        """Static method to get DB instance by it's url"""
        database = DataBaseFactory.__factory.get(database_url)
        if database:
            return database

        database = DataBase(database_url)
        DataBaseFactory.__factory[database_url] = database
        return database
