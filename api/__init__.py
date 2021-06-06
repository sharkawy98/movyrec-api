from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from importlib import import_module

db = SQLAlchemy(session_options={'expire_on_commit': False})

jwt = JWTManager()

mail = Mail()


def register_blueprints(app):
    blueprints = (
        'users',
    )
    for blueprint in blueprints:
        module = import_module(f'api.{blueprint}')
        app.register_blueprint(module.blueprint)

def config_database(app):
    @app.before_first_request
    def create_default():
        db.create_all()

def create_app(path, config):
    app = Flask(__name__, template_folder='../utils')
    app.config.from_object(config)
    app.path = path
    register_blueprints(app)
    config_database(app)
    return app
