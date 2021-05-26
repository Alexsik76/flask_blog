import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    BASE_DIR = basedir
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'app.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'DATABASE_URL') or f'postgresql+psycopg2://{DB_USER}:{DB_PW}@{DB_PATH}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = True
    # --<email config:>--
    MAIL_SERVER = 'smtp.i.ua'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'my_python@i.ua'
    MAIL_PASSWORD = 'lyedth12'
    MAIL_DEFAULT_SENDER = 'Site registration'



class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    BASE_DIR = basedir
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    # WTF_CSRF_ENABLED = False


app_config = {
    'base_config': Config,
    'testing': TestingConfig,
    'develop': DevelopmentConfig
}
