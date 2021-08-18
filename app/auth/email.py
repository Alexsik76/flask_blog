from threading import Thread
from flask import render_template, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail


def async_send_email(obj, msg):
    with obj.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            return e


def send_email(email, goal, sync=False):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    subject, template = {'registration': ('New user', 'email/register.txt'),
                         'reset': ('Reset password', 'email/reset_password.txt')}[goal]
    msg = Message(subject=subject, recipients=[email])
    msg.body = render_template(template, token=token)
    if sync:
        mail.send(msg)
    else:
        Thread(target=async_send_email, args=(current_app._get_current_object(), msg)).start()
