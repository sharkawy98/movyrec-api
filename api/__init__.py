from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy(session_options={'expire_on_commit': False})


def register_blueprints(app):
    blueprints = ()
    for blueprint in blueprints:
        module = import_module(f'api.{blueprint}')
        app.register_blueprint(module.blueprint)

def create_app(path, config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.path = path
    register_blueprints(app)

    return app
