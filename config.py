import os

SECRET_KEY = 'your-secret-key'

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'your-project-id'

# CloudSQL & SQLAlchemy configuration
CLOUDSQL_USER = 'user'
CLOUDSQL_PASSWORD = 'password'
CLOUDSQL_DATABASE = 'database-name'

# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
# You must also update the value in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'sql-instance-name'

LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

CONNECT_CLOUDSQL = False

if os.environ.get('GAE_INSTANCE') or CONNECT_CLOUDSQL:
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

basedir = os.path.abspath(os.path.dirname(__file__))

CAS_SERVER = 'https://fed.princeton.edu/cas/' 
CAS_AFTER_LOGIN = 'validate'
