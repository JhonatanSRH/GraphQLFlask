from app import db


class Book(db.Model):
    __tablename__ = "book"
    
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True)
    subtitle = db.Column(db.String(256))
    author = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    publication_date = db.Column(db.Date())
    publisher = db.Column(db.String(256))
    description = db.Column(db.String(256))
    image = db.Column(db.String(256))
    
    def __repr__(self):
        return f"<Book {self.title}>"


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))

    def __repr__(self):
        return f"<Category {self.name}>"
