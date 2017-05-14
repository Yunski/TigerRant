# TigerRant

## Overview
This project is a dedicated course shopping site for Princeton University.

The goal is provide students with a supplemental information source, such as unfiltered student reviews, an urban dictionary with course descriptions, and a yak-like real-time posting mechanism to keep shoppers and enrolled students up to speed. Students have the option of following courses and getting notifications.

Our website still provides the official course offerings information, but students now have the opportunity to read exclusive content and contribute their own.

We hope that this will make course shopping more fun and informative.
The final feature of our website is a shopping cart that syncs with a user's ReCal calendar.

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
To test the search function:
'''
$ python testing.py
'''

