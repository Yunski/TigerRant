import os

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = 'your-secret-key'

# SQLAlchemy configuration
SQL_USER = 'root'
SQL_PASSWORD = 'your-password'
SQL_DATABASE = 'your-database'

# Alternatively, you could use a local MySQL instance for testing.
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=SQL_USER, password=SQL_PASSWORD,
        database=SQL_DATABASE)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
