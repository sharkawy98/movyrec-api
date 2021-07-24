from flask import (
    request, 
    render_template,
    current_app
)
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)
from datetime import datetime
import cloudinary, cloudinary.uploader

from api.users import blueprint
from api.users.models import User, UserSchema
from utils import send_email, random_code
from api.base_models import TokenBlocklist


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

    # send verification code to user's email
    code = random_code.generate_code()
    user.activ_code = code
    user.save()

    html = render_template('activation_template.html',
        username=user.username, activation_code=code)
    subject = "Account Activation"
    send_email.send_email(user.email, subject, html)

    access_token = create_access_token(identity=user.id)

    return {
        "message": "Account is created and activation code is sent to your email",
        "access_token": access_token
    }, 200


@blueprint.route('/login', methods=['POST'])
def user_login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.get_by_username(username)

    if not user or not user.check_password(password):
        return {"message": "Username or password is incorrect"}, 401

    if not user.is_active:
        return {"message": "Your account is not activated yet."}, 403

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
    tbl = TokenBlocklist(jti=jti, created_at=datetime.now())
    tbl.save()
    return {"message": "Logged out successfully."}, 200
    

@blueprint.route('/activate', methods=['PUT'])
def user_activation():
    username = request.json.get("username")
    activ_code = request.json.get("activ_code")

    user = User.get_by_username(username)
    if user and user.activ_code != activ_code:
        return {"messege": "Wrong activation code"}, 403
    elif not user:
        return {"messege": "Wrong inputs"}, 400

    user.is_active = True
    user.update()

    return {"message": "Activated account successfully."}, 200


@blueprint.route('/forget_password', methods=['POST'])
def forget_password():
    email = request.json.get('email')
    user = User.get_by_email(email)
    if not user:
        return {"message": "Invalid email address."}, 401

    # send verification code to user's email
    code = random_code.generate_code()
    user.verif_code = code
    user.update()

    html = render_template('verification_template.html',
        username=user.username, verification_code=code)
    subject = "Reset Password"
    send_email.send_email(user.email, subject, html)

    return {"message": "Verification code is sent to your email"}, 200


@blueprint.route('/reset_password', methods=['PUT'])
def reset_password():
    username = request.json.get("username")
    new_password = request.json.get("new_password")
    verif_code = request.json.get("verif_code")

    user = User.get_by_username(username)
    if user and  user.verif_code != verif_code:
        return {"messege": "Wrong verification code"}, 403
    elif not user:
        return {"messege": "Wrong inputs"}, 400

    user.set_password(new_password)
    user.update()

    return {"message": "Reseted passsword successfully."}, 200


@blueprint.route('/display_image', methods=['PUT'])
@jwt_required()
def upload_display_image():
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower()\
            in ALLOWED_EXTENSIONS

    if 'image' not in request.files:
        return {"message": "No image selected for uploading"}, 400
    file = request.files['image']

    if file and allowed_file(file.filename):
        user = User.get_by_id(id=get_jwt_identity())

        filename = user.username

        cloudinary.config(
            cloud_name = current_app.config['CLOUD_NAME'], 
            api_key= current_app.config['API_KEY'], 
            api_secret=current_app.config['API_SECRET']
        )
        upload_result = cloudinary.uploader.upload(file=file, 
            public_id=filename)

        user.display_img = upload_result['url']
        user.update()

        return {"display_img": upload_result['url']}, 200
    else:
        return {"message": "File type not allowed, upload png, \
            jpg, jpeg, gif"}, 400
