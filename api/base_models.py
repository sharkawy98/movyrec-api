from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from api import db

class BaseModel(db.Model):
    '''Define the base model for all other models.'''
    __abstract__ = True
    id = db.Column(db.Integer(), primary_key=True)

    def save(self):
        '''Save an instance of the model to the database.'''
        try:
            db.session.add(self)
            db.session.commit()     
        except IntegrityError:
            db.session.rollback()
        except SQLAlchemyError:
            db.session.rollback()

    def update(self):
        '''Update an instance of the model on the database.'''
        return db.session.commit()

    def delete(self):
        '''Delete an instance of the model from the database.'''
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()



class ExistenceCheck():
    @classmethod
    def is_exist(cls, user_id, movie_id):
        obj = cls.query.filter_by(user_id=user_id) \
                .filter_by(movie_id=movie_id).first()
        if obj:
            return True
        return False



class TokenBlocklist(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
