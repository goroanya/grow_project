"""Module which starts REST API server"""
from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-position
from rest import APP


if __name__ == '__main__':
    APP.run(debug=True)
