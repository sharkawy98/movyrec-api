from flask import Blueprint

blueprint = Blueprint(
    'recommendations_blueprint',
    __name__,
    url_prefix='/recommendations',
)
