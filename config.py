from os import environ
from datetime import timedelta


class Config(object):
    SQLALCHEMY_DATABASE_URI = environ.get(
        'movyrek_DATABASE_URL',
        'sqlite:///db.sqlite3?check_same_thread=False'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DebugConfig(Config):
    DEBUG = True
    SECRET_KEY = environ.get(
        'movyrek_SECRET_KEY', 
        'this-is-secret'
    )

    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=183)  # 6 months
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'movyrek@gmail.com'
    MAIL_PASSWORD = 'movyrek123'
    ACTIVATION_EMAIL_SALT = 'activation-salt'

app_config_dict = {
    'Debug': DebugConfig,
}