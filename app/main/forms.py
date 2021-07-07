from flask_wtf import FlaskForm
from wtforms import StringField, TextField, FileField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextField('Posts text', validators=[DataRequired()])
    img = FileField('Load picture', validators=[DataRequired()])
    submit = SubmitField('Update')
