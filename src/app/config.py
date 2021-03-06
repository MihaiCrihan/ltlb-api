from datetime import timedelta
from os import environ

from dotenv import load_dotenv

load_dotenv('.env')

POSTGRES = {
    'user': environ.get('PG_USER'),
    'pw': environ.get('PG_PASSWORD'),
    'db': environ.get('PG_DB_NAME'),
    'host': environ.get('PG_HOST'),
    'port': environ.get('PG_PORT', 5432),
}


class FlaskConfig(object):
    PRODUCTION = environ.get('ENVIRONMENT', 'dev') == 'prod'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = environ.get('SECRET_KEY', 'secret')

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEBUG = False
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT', 'some_salt')

    DEBUG = True
    PORT = environ.get('PORT')
    HOST = environ.get('HOST')

    BACKEND_ADDRESS = environ.get('BACKEND_ADDRESS')
    STATIC_PATH = environ.get('STATIC_PATH')
    FRONTEND_ADDRESS = environ.get('FRONTEND_ADDRESS')
    PERMISSIONS = "config/permissions.json"

    REDIS_HOST = environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = environ.get('REDIS_PORT', 6379)
    REDIS_DB = environ.get('REDIS_DB', 0)
    REDIS_PASSWORD = environ.get('REDIS_PASSWORD', '')

    MONGO_HOST = environ.get('MONGO_HOST', 'localhost')
    MONGO_PORT = int(environ.get('MONGO_PORT', 27017))

    ENVIRONMENT = 'dev'

