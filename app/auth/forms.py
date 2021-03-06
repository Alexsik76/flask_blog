from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign up')


class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset password')


class NewPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'disabled': True})
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password2 = PasswordField('Repeat password',
                              validators=[DataRequired(),
                                          EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset password')


class RegistrationForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat password')
    submit = SubmitField('Register')


class UserForm(FlaskForm):
    email = StringField('Email')
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')
