import os
import click


class Config(object):
   ENV = os.environ["ENV"] if "ENV" in os.environ else "DEVELOPMENT"
   CSRF_ENABLED = True
   SECRET_KEY = "this_is_a_secret_key"
   SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
   DEBUG = True
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + os.environ.get("DB_USERNAME", 'root') + ":" \
                             + os.environ.get("DB_PASSWORD", 'admin1234') + "@" \
                             + os.environ.get("DB_HOST", '127.0.0.1') + ":" \
                             + os.environ.get("DB_PORT", '3306') + "/" \
                             + os.environ.get("DB_DATABASE", 'test')
   click.echo(SQLALCHEMY_DATABASE_URI)
   print(SQLALCHEMY_DATABASE_URI)


class TestingConfig(Config):
   DEBUG = False
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + os.environ.get("DB_USERNAME", 'root') + ":" \
                             + os.environ.get("DB_PASSWORD", 'admin1234') + "@" \
                             + os.environ.get("DB_HOST", 'localhost') + ":" \
                             + os.environ.get("DB_PORT", '3306') + "/" \
                             + os.environ.get("DB_DATABASE", 'test')