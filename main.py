from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import BooksForm, EditForm
import os

app = Flask(__name__)
# database object
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# open/create a cursor object
db = SQLAlchemy(app)
Bootstrap(app)


# creating a class to handle tables in the DB
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<title %r author %r rating %r>' % self.title % self.author % self.rating


db.create_all()


@app.route('/')
def home():
    # get the books from BOOKS object(database object)
    all_books = db.session.query(Books).all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BooksForm()
    if form.validate_on_submit() and request.method == 'POST':
        # get the data from the form using "data" on form object
        new_book = Books(title=form.title.data, author=form.author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/edit_rating/', methods=['GET', 'POST'])
def edit_rating():
    form = EditForm()
    if request.method == "POST":
        book_id = request.args.get("id")
        update_book = Books.query.get(book_id)
        update_book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("id")
    book = Books.query.get(book_id)
    return render_template('edit_rating.html', edit_form=form)


@app.route('/delete_book/', methods=['GET'])
def delete_book():
    book_id = request.args.get('id')
    del_book = Books.query.get(book_id)
    db.session.delete(del_book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
