from os import getenv
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv(
        'movyrek_DATABASE_URL',
        'sqlite:///db.sqlite3?check_same_thread=False'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DebugConfig(Config):
    DEBUG = True
    SECRET_KEY = getenv('movyrek_SECRET_KEY')

    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=183)  # 6 months
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    ACTIVATION_EMAIL_SALT = getenv('ACTIVATION_EMAIL_SALT')

    CLOUD_NAME = getenv('CLOUD_NAME')
    API_KEY = getenv('API_KEY')
    API_SECRET = getenv('API_SECRET')


app_config_dict = {
    'Debug': DebugConfig,
}