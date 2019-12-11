"""Module which starts REST API server"""
import os

from dotenv import load_dotenv

from rest import APP
from service import DataBase

if __name__ == '__main__':
    load_dotenv()
    APP.config['DATABASE'] = DataBase(os.getenv('DATABASE_URL'))
    APP.run(debug=True)
