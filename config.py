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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=183)  # 6 months
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

app_config_dict = {
    'Debug': DebugConfig,
}