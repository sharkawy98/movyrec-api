from datetime import datetime
from werkzeug.security import generate_password_hash, \
    check_password_hash

from api.base_model import BaseModel, db


class User(BaseModel):
    __tablename__ = 'users'
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.DateTime(), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    is_active = db.Column(db.Boolean(), default=False)
    display_img = db.Column(db.String(255), default=None)

    def __repr__(self):
        return f'User {self.username}'

    def __init__(self, full_name, email, username, password, 
                birthdate, gender):
        self.full_name = full_name.title()
        self.email = email.lower()
        self.username = username.lower()
        self.set_password(password)
        self.birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
        self.gender = gender.upper()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username.lower()).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email.lower()).first()
    
    @classmethod 
    def get_by_id(cls, id):                 
        return cls.query.filter_by(id=id).first()
