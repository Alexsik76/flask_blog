from threading import Thread
from flask import render_template, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail


# def send_async_email(msg):
#     mail.send(msg)
#
#
# async def send_async_registration_email(email):
#     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
#     msg = Message(subject='New user', recipients=[email])
#     msg.body = render_template('email/register.txt', token=token)
#     send_async_email(msg)


def send_email(obj, msg):
    with obj.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            return e


async def send_registration_email(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    msg = Message(subject='New user', recipients=[email])
    msg.body = render_template('email/register.txt', token=token)
    Thread(target=send_email, args=(current_app._get_current_object(), msg)).start()


async def send_reset_password_email(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    msg = Message(subject='Reset password', recipients=[email])
    msg.body = render_template('email/reset_password.txt', token=token)
    Thread(target=send_email, args=(current_app._get_current_object(), msg)).start()



