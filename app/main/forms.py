from os import path
import imghdr
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, StopValidation


class ValidateImage:
    def __init__(self, message=None):
        if not message:
            message = 'Files content is not valid!'
        self.message = message

    def __call__(self, form, field):
        def check_stream(stream):
            header = stream.read(512)
            stream.seek(0)
            file_format = imghdr.what(None, header)
            if not file_format:
                return None
            return '.' + (file_format if file_format != 'jpeg' else 'jpg')
        img = getattr(form, field.name).data
        filename = secure_filename(img.filename)
        file_ext = path.splitext(filename)[1].lower()
        from_stream_ext = check_stream(img.stream)
        if file_ext != from_stream_ext:
            raise StopValidation(self.message)


validate_image = ValidateImage()


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Posts text', validators=[DataRequired()])
    img = FileField('Load picture',
                    validators=[FileRequired(),
                                FileAllowed(['jpg', 'png', 'gif'], 'Images only!'),
                                validate_image])
    submit = SubmitField('Publish')
