from os import environ


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

app_config_dict = {
    'Debug': DebugConfig,
}