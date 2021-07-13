from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.movies import blueprint
from api.movies.models import (
    WatchList, 
    Rating, 
    Review,
    watch_list_schema,
    ratings_schema,
    reviews_schema
)



@blueprint.route('/watch_list/<movie_id>', methods=['POST'])
@jwt_required()
def add_to_watchlist(movie_id):
    user_id = get_jwt_identity()

    wl = WatchList(user_id, movie_id)
    wl.save()

    return {"message": "Added to watch_list successfuly."}, 200


@blueprint.route('/rate/<movie_id>', methods=['POST'])
@jwt_required()
def rate_movie(movie_id):
    user_id = get_jwt_identity()
    rating = request.json.get('rating')

    r = Rating(user_id, movie_id, rating)
    r.save()

    return {"message": "Rated movie successfuly."}, 200
    

@blueprint.route('/review/<movie_id>', methods=['POST'])
@jwt_required()
def review_movie(movie_id):
    user_id = get_jwt_identity()
    review = request.json.get('review')

    r = Review(user_id, movie_id, review)
    r.save()

    return {"message": "Reviewed movie successfuly."}, 200


@blueprint.route('/user_watch_list')
@jwt_required()
def get_watch_list():
    user_id = get_jwt_identity()
    watch_list = WatchList.query.filter_by(user_id=user_id).all()
    return {"watch_list": watch_list_schema.dump(watch_list)}, 200


@blueprint.route('/movie_reviews/<movie_id>')
@jwt_required()
def get_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return {"reviews": reviews_schema.dump(reviews)}, 200
