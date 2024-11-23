# src/Service/MovieMakerService.py
from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.movie_maker_dao import MovieMakerDAO
from src.Model.movie_maker import MovieMaker
from src.TMDB.movie_maker_tmdb import MovieMakerTMDB


class MovieMakerService:
    """ A MovieMaker object in our service layer.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    movie_maker_dao : MovieMakerDao
        A DAO object used for operations related to movies makers.
    movie_maker_tmdb : MovieMakerTMDB
        A movie maker   
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.movie_maker_dao = MovieMakerDAO(db_connection)
        self.movie_maker_tmdb = MovieMakerTMDB(db_connection)

    def get_movie_maker_by_name(self, name: str) -> List[MovieMaker] | None:
        """
        Retrieves a MovieMaker by their name from the database or the TMDB API.

        Parameters:
        -----------
        name : str
            The name of the MovieMaker to search for.

        Returns:
        --------
        List[MovieMaker] | None
            A list of MovieMaker object if found, otherwise None.
        """
        movie_makers = self.movie_maker_dao.get_by_name(name)
        if movie_makers:
            return movie_makers 
        else:
            movie_maker_from_tmdb = self.movie_maker_tmdb.get_movie_maker_by_name(name)
            if movie_maker_from_tmdb:
                for data in movie_maker_from_tmdb:
                    self.movie_maker_dao.insert(data)
                return movie_maker_from_tmdb
            print(f"No MovieMaker found with name: {name}.")
            return None

# db_connection = DBConnector()
# my_object = MovieMakerService(db_connection)
# print(my_object.get_movie_maker_by_name("alain chabat"))