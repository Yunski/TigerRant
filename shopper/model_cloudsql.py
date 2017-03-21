import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from migrate.versioning import api

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

# [START model]
instructors = db.Table("instructors",
    db.Column("c_id", db.Integer, db.ForeignKey("course.c_id")),
    db.Column("instructor_id", db.Integer, db.ForeignKey("instructor.emplid")),
    db.Column("review_id", db.Integer, db.ForeignKey("review.id"))
)

class Course(db.Model):
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True)
    c_id = db.Column(db.Integer, index=True, unique=True)
    dept = db.Column(db.String(3), index=True)
    catalog_number = db.Column(db.String(4), index=True)
    title = db.Column(db.UnicodeText())
    track = db.Column(db.UnicodeText())
    description = db.Column(db.UnicodeText())
    crosslistings = db.Column(db.UnicodeText())
    instructors = db.relationship("Instructor", secondary=instructors,
        backref=db.backref('courses', lazy='dynamic'))
    reviews = db.relationship('Review', backref='course',
                                lazy='dynamic')
    url = db.Column(db.UnicodeText())

    def __repr__(self):
        return "<Course {}{}>".format(self.code, self.catalog_number)

class Instructor(db.Model):
    id = db.Column(db.Integer, index=True, unique = True, primary_key = True)
    emplid = db.Column(db.Integer, index=True, unique = True)
    first_name = db.Column(db.UnicodeText())
    last_name = db.Column(db.UnicodeText())

    def __repr__(self):
        return "<Instructor {} {}>".format(self.first_name, self.last_name)

class User(db.Model):
    id = db.Column(db.Integer, index=True, unique = True, primary_key = True)
    netid = db.Column(db.Unicode(32), index=True, unique = True)
    ticket = db.Column(db.UnicodeText())
    first_name = db.Column(db.UnicodeText())
    last_name = db.Column(db.UnicodeText())

class Review(db.Model):
    id = db.Column(db.Integer, index=True, unique = True, primary_key = True)
    num = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.c_id'), index=True)
    sem_code = db.Column(db.Integer, index=True)
    overall_rating = db.Column(db.Float, index=True)
    lecture_rating = db.Column(db.Float)
    student_advice = db.Column(db.UnicodeText())
    instructors = db.relationship("Instructor", secondary=instructors,
        backref=db.backref('reviews', lazy='dynamic'))

    def __repr__(self):
        return "<Review {} {}>".format(self.c_id, self.term_id)

# [END model]

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
        SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
        SQLALCHEMY_MIGRATE_REPO = app.config.get('SQLALCHEMY_MIGRATE_REPO')
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
            print("All tables created")
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
            print("All tables created")


if __name__ == '__main__':
    _create_database()
