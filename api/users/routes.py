from flask import request, render_template, url_for
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from itsdangerous import SignatureExpired, BadTimeSignature

from api.users import blueprint
from api.users.models import User, UserSchema
from utils import activation, send_email, verification


user_schema = UserSchema()

black_list = set()


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

    # send activation link to new registered user 
    token = activation.generate_activation_token(user.email)
    confirm_url = url_for('users_blueprint.user_activation', 
        token=token, _external=True)
    
    html = render_template('activation_template.html',
        username=user.username, confirm_url=confirm_url)
    subject = "Account Activation"
    send_email.send_email(user.email, subject, html)
    
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


@blueprint.route('/user_info')
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    return user_schema.dump(user), 200


@blueprint.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    black_list.add(jti)
    return {"message": "Logged out successfully."}, 200
    

@blueprint.route('/activate/<token>')
def user_activation(token):
    try:
        email = activation.confirm_activation(token)
    except SignatureExpired:
        return '<h1>The token is expired. Register again !</h1>'
    except BadTimeSignature:
        return '<h1>Invalid token.</h1>'

    # update activation attribute in the database
    user = User.get_by_email(email)
    user.is_active = True
    user.update()

    return '<h1>Your account is activated successfully.</h1>'


@blueprint.route('/forget_password', methods=['POST'])
def forget_password():
    email = request.json.get('email')
    user = User.get_by_email(email)
    if not user:
        return {"message": "Invalid email address."}, 401

    # send verification code to user's email
    code = verification.generate_verification_code()
    user.verif_code = code
    user.update()

    html = render_template('verification_template.html',
        verification_code=code)
    subject = "Reset Password"
    send_email.send_email(user.email, subject, html)

    return {"message": "Verification code is sent"}, 200


@blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get("email")
    new_password = request.json.get("new_password")
    verif_code = request.json.get("verif_code")

    user = User.get_by_email(email)
    if user.verif_code != verif_code:
        return {"messege": "Not allowed"}, 403

    user.set_password(new_password)
    user.update()

    return {"message": "Reseted passsword successfully."}, 200
    