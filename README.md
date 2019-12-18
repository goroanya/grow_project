# Graduation work project

[![Build Status](https://travis-ci.org/traumgedanken/grow_project.svg?branch=master)](https://travis-ci.org/traumgedanken/grow_project)
[![Coverage Status](https://coveralls.io/repos/github/traumgedanken/grow_project/badge.svg?branch=master)](https://coveralls.io/github/traumgedanken/grow_project?branch=master)
## DESCRIPTION
Create a simple web application for managing departments and employees. The web application should use aforementioned web service for storing data and reading from database. One should be able to deploy the web application on Gunicorn using command line. All public functions / methods on all levels should include unit tests. Debug information should be displayed at the debugging level in the console and in a separate file. Classes and functions / methods must have docstrings comments. Finalyze README file which should contain a brief description of the project, instructions on how to build a project from the command line, how to start it, and at what addresses the Web service and the Web application will be available after launch.

## The web application should allow:

1. display a list of departments and the average salary (calculated automatically) for these departments
2. display a list of employees in the departments with an indication of the salary for each employee and a search field to search for employees born on a certain date or in the period between dates
3. change (add / edit / delete) the above data

## How to build
- Install python 3.5 or later
- Install nginx to your system: 
`sudo apt-get install nginx`
- Activate your virtual environment (optionally)
- Move to the project root directory and install python dependencies: 
`pip install -r requirements.txt`
- Configure nginx services by running:
`python config.py`
- To start application: `sudo systemctl start server.service client.service`. After that server and client will be available at http://server.test and http://client.test

#####Author
Ihor Bulaievskyi ([telegram](https://t.me/traumgedanken))

