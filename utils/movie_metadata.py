from flask import current_app
import requests


def get_metadata(movie_id):
    '''Return movie metadata from TMDB API'''
    
    url = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
    result = requests.get(url.format(
        movie_id, 
        current_app.config['TMDB_KEY']
    ))
    
    return result.json()
