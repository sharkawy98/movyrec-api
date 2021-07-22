from api.base_models import BaseModel, db, ExistenceCheck

class Movie(BaseModel):
    __tablename__ = 'movies'
    tmdb_id = db.Column(db.Integer())            
    imdb_id = db.Column(db.String(20))            
    title = db.Column(db.String(100))            
    release_date = db.Column(db.Date())
    score = db.Column(db.Float())           
    overview = db.Column(db.Text())         
    genres = db.Column(db.String(100))    
    keywords = db.Column(db.String(255))          
    cluster = db.Column(db.Integer())        

    def __repr__(self):
        return f'Movie {self.title}'


class WatchList(BaseModel, ExistenceCheck):
    __tablename__ = 'watch_list'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id


class Rating(BaseModel, ExistenceCheck):
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))
    rating = db.Column(db.Float(), nullable=False)

    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


class Review(BaseModel, ExistenceCheck):
    __tablename__ = 'reviews'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))
    review = db.Column(db.Text(), nullable=False)

    def __init__(self, user_id, movie_id, review):
        self.user_id = user_id
        self.movie_id = movie_id
        self.review = review



from marshmallow import Schema, fields

class WatchListSchema(Schema):
    movie_id = fields.Integer(dump_only=True)

class RatingsSchema(Schema):
    movie_id = fields.Integer(dump_only=True)
    rating = fields.Float(dump_only=True)

class ReviewsSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    review = fields.String(dump_only=True)


watch_list_schema = WatchListSchema(many=True)
ratings_schema = RatingsSchema(many=True)
reviews_schema = ReviewsSchema(many=True)
