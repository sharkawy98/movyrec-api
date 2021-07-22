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
from utils.movie_metadata import get_metadata


@blueprint.route('/watch_list/<movie_id>', methods=['POST'])
@jwt_required()
def add_to_watchlist(movie_id):
    user_id = get_jwt_identity()

    if WatchList.is_exist(user_id, movie_id):
        return {"message": "You added this movie before."}, 409

    wl = WatchList(user_id, movie_id)
    wl.save()

    return {"message": "Added to watch_list successfuly."}, 200


@blueprint.route('/rate/<movie_id>', methods=['POST'])
@jwt_required()
def rate_movie(movie_id):
    user_id = get_jwt_identity()

    if Rating.is_exist(user_id, movie_id):
        return {"message": "You rated this movie before."}, 409

    rating = request.json.get('rating')
    r = Rating(user_id, movie_id, rating)
    r.save()

    return {"message": "Rated movie successfuly."}, 200
    

@blueprint.route('/review/<movie_id>', methods=['POST'])
@jwt_required()
def review_movie(movie_id):
    user_id = get_jwt_identity()

    if Review.is_exist(user_id, movie_id):
        return {"message": "You reviewed this movie before."}, 409

    review = request.json.get('review')
    r = Review(user_id, movie_id, review)
    r.save()

    return {"message": "Reviewed movie successfuly."}, 200


@blueprint.route('/user_watch_list')
@jwt_required()
def get_watch_list():
    user_id = get_jwt_identity()
    watch_list = WatchList.query.filter_by(user_id=user_id).all()

    result = []
    for m in watch_list:
        result.append(get_metadata(m.movie_id))

    return {"watch_list": result}, 200


@blueprint.route('/user_ratings')
@jwt_required()
def get_ratings():
    user_id = get_jwt_identity()
    ratings = Rating.query.filter_by(user_id=user_id).all()

    result = []
    for r in ratings:
        result.append(get_metadata(r.movie_id))

    return {"ratings": result}, 200


@blueprint.route('/movie_interactions/<movie_id>')
@jwt_required()
def get_movie_interactions(movie_id):
    user_id = get_jwt_identity()

    rating = Rating.query.filter_by(movie_id=movie_id) \
        .filter_by(user_id=user_id).first()
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    
    return {
        "user_rating": rating.rating,
        "movie_reviews": reviews_schema.dump(reviews)
    }, 200


@blueprint.route('/watch_list/<movie_id>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(movie_id):
    user_id = get_jwt_identity()
    wl = WatchList.query.filter_by(movie_id=movie_id) \
        .filter_by(user_id=user_id).first()
    wl.delete()
    return {"message": "Removed from watch_list successfuly."}, 200


@blueprint.route('/review/<movie_id>', methods=['DELETE'])
@jwt_required()
def remove_review(movie_id):
    user_id = get_jwt_identity()
    r = Review.query.filter_by(movie_id=movie_id) \
        .filter_by(user_id=user_id).first()
    r.delete()
    return {"message": "Removed your review successfuly."}, 200


@blueprint.route('/rate/<movie_id>', methods=['PATCH'])
@jwt_required()
def update_rating(movie_id):
    user_id = get_jwt_identity()
    new_rating = request.json.get('rating')

    r = Rating.query.filter_by(movie_id=movie_id) \
        .filter_by(user_id=user_id).first()
    r.rating = new_rating
    r.update()
    return {"message": "Updated your rating successfuly."}, 200
