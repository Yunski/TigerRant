import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128))

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
