
import graphene

from app import db
from app.graphql.object import Book as Book, Category as Category
from app.graphql.query import get, instance_books
from app.models import Book as BookModel, Category as CategoryModel

class BookMutation(graphene.Mutation):
    
    class Arguments:
        title = graphene.String(required=True)
        subtitle = graphene.String(required=True)
        author = graphene.String(required=True)
        publication_date = graphene.Date(required=True)
        publisher = graphene.String(required=True)
        description = graphene.String(required=True)
        category_id = graphene.Int(required=True)

    book = graphene.Field(lambda: Book)

    def mutate(self, info, title, subtitle, author, publication_date, publisher, description, category_id):
        book = BookModel(title=title, subtitle=subtitle, author=author, publication_date=publication_date, publisher=publisher, description=description, category_id=category_id)

        db.session.add(book)
        db.session.commit()

        return BookMutation(book=book)

class BookSourceMutation(graphene.Mutation):
    
    class Arguments:
        book_id = graphene.Int(required=True)
        source = graphene.String(required=True)

    book = graphene.Field(lambda: Book)

    def mutate(self, info, book_id, source=1):
        if source == 1:
            google_result = get('https://www.googleapis.com/books/v1/volumes/{}'.format(book_id))
            book = instance_books(google_result, 1)
        if source == 2:
            api_result = get('https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?isbn={}api-key=7ZOgGGznc9VlmTPVAZKvc4HVejWL4jyQ'.format(book_id))
            book = instance_books(api_result.get('books', []), 2)
        return BookMutation(book=book)

class DeleteBook(graphene.Mutation):

    class Arguments:
        book_id = graphene.Int(required=True)

    book = graphene.Field(lambda: Book)
    
    def mutate(self, info, **kwargs):
        query = Book.get_query(info)
        query = query.filter(BookModel.book_id==kwargs['book_id'])
        query_result = query.all()
        query.delete()
        db.session.commit()
        return query_result

class CategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String(required=True)

    category = graphene.Field(lambda: Category)

    def mutate(self, info, name):
        category = CategoryModel(name=name)

        db.session.add(category)
        # Update book
        db.session.commit()

        return CategoryMutation(category=category)

class Mutation(graphene.ObjectType):
    mutate_book = BookMutation.Field()
    delete_book = DeleteBook.Field()
    mutate_category = CategoryMutation.Field()
    mutate_source = BookSourceMutation.Field()