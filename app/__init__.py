from flask import Flask
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
   app = Flask(__name__)

   @app.route("/")
   def test():
       return "Test ok!"

   return app