"""Module which starts REST API server"""
from rest.app import APP as app

if __name__ == '__main__':
    app.run(debug=True)
