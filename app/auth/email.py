from flask import render_template, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import mail


async def send_registration_email(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    msg = Message(subject='New user', recipients=[email])
    msg.body = render_template('email/register.txt', token=token)
    mail.send(msg)
