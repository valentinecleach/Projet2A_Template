# src/Service/MovieMakerService.py
from src.DAO.movie_maker_dao import MovieMakerDAO
from src.TMDB.movie_maker_tmdb import MovieMakerTMDB
from src.Model.movie_maker import MovieMaker
from src.DAO.db_connection import DBConnector
from typing import List


class MovieMakerService:
    def __init__(self, db_connection: DBConnector):
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
        # Firstly, we look for the MovieMaker in the database
        movie_makers = self.movie_maker_dao.get_by_name(name)
        if movie_makers:
            return movie_makers # a list of 1 or many movie maker
        # If not in our database, we look for the MovieMaker in the TMDB api.
        else:
            movie_maker_from_tmdb = self.movie_maker_tmdb.get_movie_maker_by_name(name)
            if movie_maker_from_tmdb:
                for data in movie_maker_from_tmdb:
                    self.movie_maker_dao.insert(data)
                return movie_maker_from_tmdb

            # Si rien n'est trouvé
            print(f"No MovieMaker found with name: {name}.")
            return None

# db_connection = DBConnector()
# my_object = MovieMakerService(db_connection)
# print(my_object.get_movie_maker_by_name("alain chabat"))