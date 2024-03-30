from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db = SQLAlchemy(app)

class Format(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String(20), nullable=False)
    book = db.relationship("Book", backref="format", uselist=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), unique=True, nullable=False)
    year = db.Column(db.Date, nullable=False)
    format_id = db.Column(db.Integer, db.ForeignKey("format.id"))
    authors = db.relationship("Author", back_populates="book")


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auhor_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", back_populates="author")


@app.route("/")
def index():
    return "/get_certificate/Pylyp /get_crew/Victoria"


@app.route("/get_authors/<book_name>", methods=["GET"])
def get_authors(book_name):
    book = Book.query.filter_by(name=book_name).first()
    if book:
        authors = [author.name for author in book.authors]
        return authors
    return "Book not found"


@app.route("/get_book/<author_name>", methods=["GET"])
def get_book(author_name):
    author = Author.query.filter_by(name=author_name).first()
    if author:
        return author.book.name
    return "Author not found"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)