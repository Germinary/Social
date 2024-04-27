from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms import SubmitField

class PostForm(FlaskForm):
    content = TextAreaField('Контент', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')