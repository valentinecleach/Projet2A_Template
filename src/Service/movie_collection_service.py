from typing import List, Dict
from src.Model.movie_collection import MovieCollection

class MovieCollectionService:
    def __init__(self):
        pass

    @classmethod    
    def create_list_of_collection(cls, movie_collection_data : dict) -> List[MovieCollection]: # list of collection to be more complete than TMDB API wich has only 1 collection by Movie.
        """ create a list of collection with a dictionnary"""
        return [MovieCollection(movie_collection_data)]