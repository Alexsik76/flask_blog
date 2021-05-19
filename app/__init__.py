from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flaskext.markdown import Markdown


db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    csrf.init_app(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    Markdown(app)

    db.init_app(app)

    # from app.create_db import init_app
    # init_app(app)

    from app.main import bp
    app.register_blueprint(bp)

    return app


