import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from os import path


dirname = path.dirname(__file__)


def load_cluster_movies(data, movie_id):
	cluster = data[data['tmdb_id']==movie_id].cluster.values[0]
	cluster_movies = data.loc[data['cluster'] == cluster] 
	cluster_movies = cluster_movies.reset_index(drop=True)
	return cluster_movies


def get_similarities(data):
    tfidf = TfidfVectorizer(
      min_df=2,
      max_df=0.7,
      ngram_range=(1,3), 
      stop_words='english'
    )
    tfidf_matrix = tfidf.fit_transform(data['overview'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def get_movie_recommendations(movie_id, data, similarities):
	indices = pd.Series(data.index, index=data['tmdb_id'])

	movie_idx = indices[movie_id]
	sim_scores = list(enumerate(similarities[movie_idx]))
	sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
	sim_scores = sim_scores[1:6]
	recommendations_indices = [i[0] for i in sim_scores]
	return data.iloc[recommendations_indices]


def get_user_recommendations(user_ratings):
	'''Return IDs of the top 5 recommended movies'''
	movies = pd.read_csv(path.join(dirname, 'movies.csv'))
	recommendations = pd.DataFrame()

	for r in user_ratings:
		if r.rating >= 3:
			movie_id = r.movie_id

			cluster_movies = load_cluster_movies(movies, movie_id)
			similarities = get_similarities(cluster_movies)

			if movie_id not in (cluster_movies['tmdb_id']).values:
				continue
			else:
				recommendations = recommendations.append(
					get_movie_recommendations(movie_id, cluster_movies, similarities)
				)
			
	recommendations = recommendations.drop_duplicates()
	recommendations = recommendations.sort_values(
		by='score', 
		ascending=False
	)    
	return recommendations['tmdb_id'].values
