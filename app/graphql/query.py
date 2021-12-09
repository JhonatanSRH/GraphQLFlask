import graphene
import requests
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from app.graphql.object import Book as Book, Category as Category
from app.models import Book as BookModel


def get(url, token=None):
    response = requests.get(url, headers={"Authorization": token})
    if response.status_code == 200:
        return response.json()
    return None

def instance_books(data_list, option, **kwargs):
    instances = []
    if option == 1:
        for data in data_list:
            if kwargs.get('mutate'):
                book = BookModel(title=data['volumeInfo'].get('title', ''), 
                                 subtitle=data['volumeInfo'].get('subtitle', ''),
                                 author=data['volumeInfo'].get('authors', [''])[0],
                                 publication_date=data['volumeInfo'].get('publishedDate', ''), 
                                 publisher=data['volumeInfo'].get('industryIdentifiers', [{}])[0].get('identifier', ''),
                                 description=data['volumeInfo'].get('description', ''),
                                 category_id=option)
            else:
                book = BookModel(book_id=data['id'], 
                                 title=data['volumeInfo'].get('title', ''), 
                                 subtitle=data['volumeInfo'].get('subtitle', ''),
                                 author=data['volumeInfo'].get('authors', [''])[0],
                                 publication_date=data['volumeInfo'].get('publishedDate', ''), 
                                 publisher=data['volumeInfo'].get('industryIdentifiers', [{}])[0].get('identifier', ''),
                                 description=data['volumeInfo'].get('description', ''),
                                 category_id=option)
            instances.append(book)
    if option == 2:
        for data in data_list:
            if kwargs.get('mutate'):
                book = BookModel(title=data.get('title', ''), 
                                 subtitle=data.get('title', ''), 
                                 author=data.get('author', ''), 
                                 publication_date=data.get('ranks_history', [{}])[0].get('published_date', '2021-01-01'), 
                                 publisher=data.get('publisher', ''),
                                 description=data.get('description', ''),
                                 category_id=option)
            else:
                book = BookModel(book_id=data['primary_isbn13'], 
                                 title=data.get('title', ''), 
                                 subtitle=data.get('title', ''), 
                                 author=data.get('author', ''), 
                                 publication_date=kwargs.get('publishedDate', ''), 
                                 publisher=data.get('publisher', ''),
                                 description=data.get('description', ''),
                                 category_id=option)
            instances.append(book)
    return instances

class Query(graphene.ObjectType):
    node = relay.Node.Field()

    books = graphene.List(lambda: Book, book_id=graphene.Int(),title=graphene.String(), subtitle=graphene.String(), 
                          author=graphene.String(), publication_date=graphene.Date(), 
                          publisher=graphene.String(), description=graphene.String(), 
                          category_id=graphene.Int())

    def resolve_books(self, info, title=None, subtitle=None, 
                      author=None, publication_date=None, publisher=None, 
                      description=None, category_id=None):
        query = Book.get_query(info)
        google_query_params = ['', '+subject']
        api_date_query_params = 'current'
        if title:
            query = query.filter(BookModel.title==title)
            google_query_params[0] = title
            google_query_params[1] = '+intitle'
        if subtitle:
            query = query.filter(BookModel.subtitle==subtitle)
            google_query_params[0] = title
            google_query_params[1] = '+intitle'
        if author:
            query = query.filter(BookModel.author==author)
            google_query_params[0] = author
            google_query_params[1] = '+inauthor'
        if publication_date:
            query = query.filter(BookModel.publication_date==publication_date)
            google_query_params[0] = publication_date
            api_date_query_params = publication_date
        if publisher:
            query = query.filter(BookModel.publisher==publisher)
            google_query_params[0] = publisher
            google_query_params[1] = '+inpublisher'
        if description:
            query = query.filter(BookModel.description==description)
            google_query_params[0] = description
        if category_id:
            query = query.filter(BookModel.category_id==category_id)
            google_query_params[0] = category_id
        query_result = query.all()
        if not len(query_result):
            google_result = get('https://www.googleapis.com/books/v1/volumes?q={}{}&filter=full&maxResults=40'.format(*google_query_params))            
            if not google_result:
                api_query_params = get('https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=7ZOgGGznc9VlmTPVAZKvc4HVejWL4jyQ')
                api_result = []
                if api_query_params:
                    api_query_params = [data.get('list_name_encoded') for data in api_query_params.get('results', [])]
                    for data in api_query_params:
                        api_result_category = get('https://api.nytimes.com/svc/books/v3/lists/{}/{}.json?api-key=7ZOgGGznc9VlmTPVAZKvc4HVejWL4jyQ'.format(api_date_query_params, data))
                        if api_result_category:
                            api_result += api_result_category.get('results', {}).get('books', [])
                if not len(api_result):
                    return query_result
                return instance_books(api_result, 2)
            return instance_books(google_result.get('items', []), 1)
        return query_result

    categories = SQLAlchemyConnectionField(Category)


    