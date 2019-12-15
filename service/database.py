"""Module contains universal class for data manipulating in DB"""
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BaseClass, Employee


class DataBase:
    """Class to work with DB"""

    def __init__(self, db_url):
        engine = create_engine(db_url)
        BaseClass.metadata.create_all(engine)
        self.session = sessionmaker(engine)()

    def get(self, cls, criterion=None, offset=None, limit=None):
        """Get all entities of cls
        @param cls: class object of entities
        @param criterion: condition
        @param offset: how many to skip
        @param limit: how many entities is maximum
        @return: list of entities
        """
        try:
            objects = self.session.query(cls)
            if criterion is not None:
                objects = objects.filter(criterion)
            if offset is not None:
                objects = objects.offset(offset)
            if limit is not None:
                objects = objects.limit(limit)
            return list(objects)
        except:
            self.session.rollback()
        finally:
            self.session.commit()

    def get_one(self, **kwargs):
        """Get only one entity of cls
        @param kwargs: like in get() method
        @return: only one entity object or None
        """
        try:
            return self.get(**kwargs)[0]
        except IndexError:
            return None
        except:
            self.session.rollback()
        finally:
            self.session.commit()

    def insert(self, obj):
        """Insert new cls object with fields from values
        @param obj: object to be inserted
        @return: same object, but updated after inserting
        """
        try:
            self.session.add(obj)
            self.session.flush()
            return obj
        except:
            self.session.rollback()
        finally:
            self.session.commit()

    def update(self, cls, criterion, date_of_birth=None, **new_values):
        """Update
        @param cls: class object
        @param criterion: condition
        @param date_of_birth: one of new values
        @param new_values: valued to be updated
        """
        try:
            if date_of_birth and not isinstance(date_of_birth, datetime.date):
                date_of_birth = Employee.date_from_str(date_of_birth)
            for obj in self.session.query(cls).filter(criterion):
                for key, value in new_values.items():
                    setattr(obj, key, value)
                if date_of_birth:
                    setattr(obj, 'date_of_birth', date_of_birth)
        except:
            self.session.rollback()
        finally:
            self.session.commit()

    def delete(self, cls, criterion):
        """Delete object
        @param cls: class object
        @param criterion: condition
        """
        try:
            self.session.query(cls).filter(criterion).delete()
        except:
            self.session.rollback()
        finally:
            self.session.commit()
