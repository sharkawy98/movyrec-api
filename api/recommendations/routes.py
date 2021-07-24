from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import random

from api.recommendations import blueprint
from api.movies.models import Rating
from utils.recommendation import get_user_recommendations
from utils.movie_metadata import get_metadata



@blueprint.route('/')
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()

    user_ratings = Rating.query.filter_by(user_id=user_id).all()

    tmdb_ids = get_user_recommendations(user_ratings)
    
    recommendations = []
    for movie_id in tmdb_ids:
        recommendations.append(get_metadata(movie_id))

    if len(recommendations) > 25:
        recommendations = random.sample(recommendations, 25)
    
    random.shuffle(recommendations)
    return {'movies': recommendations}, 200
