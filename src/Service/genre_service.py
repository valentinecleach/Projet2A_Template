from src.Model.genre import Genre
from typing import List,Dict

class GenreService:
    def __init__(self):
        pass

    @classmethod 
    def create_list_of_genre(cls, genre_data : List[Dict]) -> List[Genre]:
        """    to create a list of Genre with a list of dictionnary representing genre     """
        list_of_genre = []
        for data in genre_data:
            list_of_genre.append(Genre(data))
        return list_of_genre