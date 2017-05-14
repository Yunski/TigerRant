# TigerRant

## Overview
TigerRant is a platform for students to anonymously rant and talk about Princeton courses. 

Each course has its own page with “urban dictionary”-style course descriptions that describe what a course is really like (e.g. “learn how to learn new programming languages and tools” for COS 333), course reviews unfiltered by the Registrar, and a YikYak-style rant space for leaving “real-talk” comments. You’ll be able to see how thoughts on a course change over time and see why people drop a course! Even talk and give advice on a course before it’s started or talk about how valuable a course was for you long after you’ve taken it! 

We hope to supplement course offerings and improve the course shopping experience at Princeton!

![alt text](https://raw.githubusercontent.com/Yunski/TigerRant/master/shopper/static/img/screenshot.png)

http://tigerrant-166318.appspot.com/

## Setup
#### Getting Started
```
$ git clone https://github.com/Yunski/project-tigershop.git
$ cd project-tigershop
```
To set up a virtual environment, run the commands:
```
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate
```
Install requirements with pip:
```
$ pip install -r requirements.txt
```
#### Dependencies
This project uses [Flask-CAS](https://github.com/cameronbwhite/Flask-CAS) for authentication.

A manual install is required as the pip version has a bug with Princeton's CAS system.
In the project-tigershop directory, run the commands:
```
$ git clone https://github.com/cameronbwhite/Flask-CAS.git
$ cd Flask-CAS
$ python setup.py install
```
#### Database
To set up database, install MySQL and edit config.py with your database name, user, and password.
Then run the scripts:
```
$ python shopper/model_cloudsql.py
$ python db_populate.py
```
This project uses Alembic migrations. 

To create migration folder:
```
$ python manage.py db init
```
To generate an initial migration:
```
$ python manage.py db migrate
```
To apply the migration:
```
$ python manage.py db upgrade
```
#### Run
To run server, run the main script:
```
$ python main.py
```
#### Testing
To test the search function, run the testing script:
```
$ python testing.py
```

