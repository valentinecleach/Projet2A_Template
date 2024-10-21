from typing import List, Dict
from src.Model.movie_collection import MovieCollection

class MovieCollectionService:
    def __init__(self):
        pass

    @classmethod    
    def create_list_of_collection(cls, movie_collection_data : dict) -> List[MovieCollection]: # list of collection to be more complete than TMDB API wich has only 1 collection by Movie.
        """ create a list of collection with a dictionnary"""
        return [MovieCollection(movie_collection_data)]

movie_collection_service = MovieCollectionService()
# print(movie_collection_service.create_list_of_collection({'id': 87096, 'name': 'Avatar Collection', 'poster_path': '/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg', 'backdrop_path': '/gxnvX9kF7RRUQYvB52dMLPgeJkt.jpg'}))
print(movie_collection_service.create_list_of_collection({'id': 87096, 'name': 'Avatar Collection', 'poster_path': '/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg'}))