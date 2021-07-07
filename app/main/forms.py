from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Posts text', validators=[DataRequired()])
    img = FileField('Load picture',
                    validators=[FileRequired(),
                                FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Update')
