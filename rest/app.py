"""Module to initialize app"""
import os

from flask import Flask
from dotenv import load_dotenv

from service import DataBase

APP = Flask(__name__)
load_dotenv()
APP.config['DATABASE'] = DataBase(os.getenv('DATABASE_URL') or 'sqlite:///')
