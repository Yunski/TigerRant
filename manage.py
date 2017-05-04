from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from shopper.model_cloudsql import db
import shopper
import config

app = shopper.create_app(config)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

'''
Create migration respository:
python manage.py db init
Everytime the database models change, repeat the following commands:
python manage.py db migrate
python manage.py db upgrade
For help:
python manage.py db --help
'''
