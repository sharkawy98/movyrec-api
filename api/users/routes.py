from flask import request
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity
)

from api.users import blueprint
from api.users.models import User, UserSchema


user_schema = UserSchema()

@blueprint.route('/register', methods=['POST'])
def user_register():
    data = request.get_json()
    
    try:
        user_schema.load(data)
    except ValidationError as err:
        return err.messages, 422

    # Check if username or email exists before registration
    if User.get_by_username(data["username"]):
        return {"message": "Username already exists."}, 409
    if User.get_by_email(data["email"]):
        return {"message": "Email already exists."}, 409

    user = User(**data)
    user.save()
    
    return user_schema.dump(user), 201


@blueprint.route('/login', methods=['POST'])
def user_login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.get_by_username(username)

    if not user or not user.check_password(password):
        return {"message": "Username or password is incorrect"}, 401

    # if not user.is_active:
    #     return {"message": "Your account is not activated yet."}, 403

    access_token = create_access_token(identity=user.id)

    return {"access_token": access_token}, 200
