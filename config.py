import os
from distutils.util import strtobool
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


def get_path_safe(path, folder):
    if not os.path.isdir(os.path.join(path, folder)):
        os.mkdir(os.path.join(path, folder))
    return os.path.join(path, folder)


class Config(object):
    SECRET_KEY = 'dev'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    # SESSION_PERMANENT = False
    # --<upload config:>--
    BASE_DIR = basedir
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10
    UPLOAD_EXTENSIONS = ['jpg', 'png', 'gif']
    UPLOAD_PATH = get_path_safe(BASE_DIR, 'users_data')
    # --<database config:>--
    SQLALCHEMY_DATABASE_URI = get_env_variable('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)
    # --<email config:>--
    MAIL_SERVER = get_env_variable('MAIL_SERVER')
    MAIL_PORT = get_env_variable('MAIL_PORT')
    MAIL_USE_TLS = get_env_variable('MAIL_USE_TLS')
    MAIL_USE_SSL = get_env_variable('MAIL_USE_SSL')
    MAIL_USERNAME = get_env_variable('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_variable('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = get_env_variable('MAIL_DEFAULT_SENDER')
    MAIL_SUPPRESS_SEND = True
    MAIL_DEBUG = True
    # --<admin config:>--
    ADMIN_EMAIL = 'alex@jurist.vn.ua'


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_DEBUG = True


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
