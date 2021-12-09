import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Book as BookModel, Category as CategoryModel

class Book(SQLAlchemyObjectType):
    class Meta:
        model = BookModel
        interfaces = (relay.Node,)

class Category(SQLAlchemyObjectType):
    class Meta:
        model = CategoryModel
        interfaces = (relay.Node,)
