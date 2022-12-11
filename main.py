from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
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
# todo: refactor this
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<title %r author %r rating %r>' % self.title % self.author % self.rating


db.create_all()


# form for wtf form to handle data at UI
class BooksForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Change Rating')


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BooksForm()
    if form.validate_on_submit() and request.method == 'POST':
        new_book = Books(title=form.title.data, author=form.author.data, rating=form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/edit_rating/<int:id>', methods=['GET', 'POST'])
def edit_rating(id):
    form = EditForm()
    return render_template('edit_rating.html', id=id, form=form)


if __name__ == "__main__":
    app.run(debug=True)
