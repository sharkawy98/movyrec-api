from api.base_model import BaseModel, db


class Movie(BaseModel):
    __tablename__ = 'movies'
    tmdb_id = db.Column(db.Integer())    
    imdb_id = db.Column(db.String(20))         
    title = db.Column(db.String(100))
    overview = db.Column(db.Text())
    release_date = db.Column(db.Date())
    runtime = db.Column(db.Float())
    vote_average = db.Column(db.Float())
    vote_count = db.Column(db.Float())

    def __repr__(self):
        return f'Movie {self.title}'


class WatchList(BaseModel):
    __tablename__ = 'watch_list'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id


class Rating(BaseModel):
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))
    rating = db.Column(db.Float(), nullable=False)

    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


class Review(BaseModel):
    __tablename__ = 'reviews'
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.tmdb_id'))
    review = db.Column(db.Text(), nullable=False)

    def __init__(self, user_id, movie_id, review):
        self.user_id = user_id
        self.movie_id = movie_id
        self.review = review
