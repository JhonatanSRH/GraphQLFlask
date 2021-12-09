import os
import click


class Config(object):
   if os.getenv('GAE_ENV', '').startswith('standard'):
      ENV = 'TESTING'
   else:
      ENV = 'DEVELOPMENT'
   CSRF_ENABLED = True
   SECRET_KEY = 'this_is_a_secret_key'
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   SECRET_KEY = 'miclave'
   JWT_SECRET_KEY = 'miclave'


class DevelopmentConfig(Config):
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.environ.get('DB_USERNAME', 'root') + ':' \
                             + os.environ.get('DB_PASSWORD', 'admin1234') + '@' \
                             + os.environ.get('DB_HOST', '127.0.0.1') + ':' \
                             + os.environ.get('DB_PORT', '3306') + '/' \
                             + os.environ.get('DB_DATABASE', 'test')
   click.echo(SQLALCHEMY_DATABASE_URI)

class TestingConfig(Config):
   DEBUG = False
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + os.environ.get('DB_USERNAME', 'root') + ':' \
                             + os.environ.get('DB_PASSWORD', 'Hdh7L4dgschj8d1e') + '@' \
                             + os.environ.get('DB_HOST', '/cloudsql/flask-graphql-334616:us-central1:db-flask') + ':' \
                             + os.environ.get('DB_PORT', '3306') + '/' \
                             + os.environ.get('DB_DATABASE', 'test')