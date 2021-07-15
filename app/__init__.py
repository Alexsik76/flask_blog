from flask import Flask, flash, render_template
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, user_logged_in
from flask_admin import Admin
from flask_mail import Mail
from flaskext.markdown import Markdown
from turbo_flask import Turbo


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
from app.auth.admin import MyHomeView
admin = Admin(name='flask_main', template_mode='bootstrap4', index_view=MyHomeView())
turbo = Turbo()


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

    from app.main import bp
    app.register_blueprint(bp)
    from app.auth import bp
    app.register_blueprint(bp)

    turbo.init_app(app)

    @user_logged_in.connect_via(app)
    def login_info(sender, user):
        message = f'User logged. {sender}, {user}'
        print(message)
        flash(message, 'info')
        turbo.push(turbo.replace(render_template('auth/_user_logged.html', user=user), 'user-logged-info'))

    return app


from app import models
