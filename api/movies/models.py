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
