from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    image = FileField('Изменить изображение', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')