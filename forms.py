from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


# form for wtf form to handle data at UI
class BooksForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Add Book')


class EditForm(FlaskForm):
    rating = IntegerField('New Rating', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Change Rating')
