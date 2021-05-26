from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from flaskext.markdown import Markdown


db = SQLAlchemy()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    csrf.init_app(app)
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    Markdown(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # from app.create_db import init_app
    # init_app(app)

    from app.main import bp
    app.register_blueprint(bp)

    return app


