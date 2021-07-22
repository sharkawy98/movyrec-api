from api.base_models import BaseModel, db, ExistenceCheck       


class Recommendations(BaseModel, ExistenceCheck):
    __tablename__ = 'recommendations'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id



from marshmallow import Schema, fields

class RecommendationsSchema(Schema):
    movie_id = fields.Integer(dump_only=True)

recommendations_schema = RecommendationsSchema(many=True)
