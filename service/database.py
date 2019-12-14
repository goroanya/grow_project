"""Module contains universal class for data manipulating in DB"""
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BaseClass, Employee

class DataBase:
    """Class to work with DB"""
    def __init__(self, db_url):
        level = 'AUTOCOMMIT' if 'postgres' in db_url else None
        engine = create_engine(db_url, isolation_level=level)
        BaseClass.metadata.create_all(engine)
        self.session = sessionmaker(engine)()

    def get(self, cls, criterion=None, offset=None, limit=None):
        """Get all entities of cls"""
        objects = self.session.query(cls)
        if criterion is not None:
            objects = objects.filter(criterion)
        if offset is not None:
            objects = objects.offset(offset)
        if limit is not None:
            objects = objects.limit(limit)
        return list(objects)

    def get_one(self, **kwargs):
        """Get only one entity of cls"""
        try:
            return self.get(**kwargs)[0]
        except IndexError:
            return None

    def insert(self, obj):
        """Insert new cls object with fields from values"""
        self.session.add(obj)

    def update(self, cls, criterion, date_of_birth=None, **new_values):
        """Update"""
        if date_of_birth and not isinstance(date_of_birth, datetime.date):
            date_of_birth = Employee.date_from_str(date_of_birth)
        for obj in self.session.query(cls).filter(criterion):
            for key, value in new_values.items():
                setattr(obj, key, value)
            if date_of_birth:
                setattr(obj, 'date_of_birth', date_of_birth)

    def delete(self, cls, criterion):
        """Delete"""
        self.session.query(cls).filter(criterion).delete()
