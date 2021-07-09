from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_admin import Admin

from flask_mail import Mail
from flaskext.markdown import Markdown


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
admin = Admin(name='flask_main', template_mode='bootstrap4')


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    from app.models import User, Post
    from app.auth.admin import AppUserModelView, AppPostModelView
    admin.add_view(AppUserModelView(User, db.session))
    admin.add_view(AppPostModelView(Post, db.session))
    Markdown(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    # from app.create_db import init_app
    # init_app(app)

    from app.main import bp
    app.register_blueprint(bp)
    from app.auth import bp
    app.register_blueprint(bp)

    return app


from app import models
