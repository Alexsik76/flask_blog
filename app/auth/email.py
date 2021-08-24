from flask import render_template, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mailing import Message
from app import mail


async def send_email(email, goal):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    subject, template = {'registration': ('New user', 'email/register.txt'),
                         'reset': ('Reset password', 'email/reset_password.txt')}[goal]
    message = Message(
        subject=subject,
        recipients=[email],
        )
    message.body = render_template(template, token=token)

    await mail.send_message(message)
    return "Success"
