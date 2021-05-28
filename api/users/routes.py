from flask import request
from marshmallow import ValidationError

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
