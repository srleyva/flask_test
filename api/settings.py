import os

# Custom API
LOGGING_CONF = os.environ.get('API_LOGGING_CONF', '../logging.conf')

# Flask settings
FLASK_SERVER_NAME = os.environ.get('API_SERVER_NAME', 'localhost:8888')
FLASK_DEBUG = os.environ.get('API_DEBUG', False)

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'API_DATABASE_URI',
    'postgres://postgres:@postgres:5432/circle_test')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret-key')
