from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_activation_token(email):
    serializer = URLSafeTimedSerializer(
        current_app.config['SECRET_KEY']
    )
    return serializer.dumps(
        email, 
        salt=current_app.config['ACTIVATION_EMAIL_SALT']
    )
