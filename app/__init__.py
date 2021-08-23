import logging
from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from turbo_flask import Turbo

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
turbo = Turbo()


def create_app(config='base_config'):
    app = Flask(__name__)
    app.config.from_object(app_config[config])
    app.logger.setLevel(logging.INFO)
    print(dir(app.config))
    print(app.config.items())
    print(app.config['MAIL_DEBUG'])
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    turbo.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp
    app.register_blueprint(bp)

    from app.auth import bp
    app.register_blueprint(bp)

    from app.auth.extensions import live_log_in_info
    live_log_in_info(app)

    return app


from app import models
