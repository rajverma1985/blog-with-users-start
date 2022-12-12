from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


# form for wtf form to handle data at UI
class BooksForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    rating = IntegerField('New Rating', validators=[DataRequired()])
    submit = SubmitField('Change Rating')