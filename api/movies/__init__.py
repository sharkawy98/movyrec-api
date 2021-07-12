from flask import Blueprint

blueprint = Blueprint(
    'movies_blueprint',
    __name__,
    url_prefix='/movies',
)
