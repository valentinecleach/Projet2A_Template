# src/Service/MovieMakerService.py
from src.DAO.movie_maker_dao import MovieMakerDAO
from src.TMDB.movie_maker_tmdb import MovieMakerTMDB
from src.Model.movie_maker import MovieMaker
from datetime import datetime


class MovieMakerService:
    def __init__(self):
        self.movie_maker_dao = MovieMakerDAO()
        self.movie_maker_tmdb = MovieMakerTMDB()

    def get_movie_maker_by_name(self, name: str) -> MovieMaker | None:
        """
        Retrieves a MovieMaker by their name from the database or the TMDB API.

        Parameters:
        -----------
        name : str
            The name of the MovieMaker to search for.

        Returns:
        --------
        MovieMaker | None
            A MovieMaker object if found, otherwise None.
        """
        # Firstly, we look for the MovieMaker in the database
        movie_makers = self.movie_maker_dao.get_by_name(name)

        if movie_makers:
            return movie_makers # a list of 1 or many MovieMakers

        # If not in our database, we look for the MovieMaker in the TMDB api.
        movie_maker_from_tmdb = self.movie_maker_tmdb.get_movie_maker_by_name(name)
        
        if movie_maker_from_tmdb:
            for data in movie_maker_from_tmdb:
                self.movie_maker_dao.insert(data)
            return movie_maker_from_tmdb

        # Si rien n'est trouvé
        print(f"No MovieMaker found with name: {name}.")
        return None

    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Helper method to validate the date format (YYYY-MM-DD)."""
        if not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")  # check if str can be convert to valid datetime
            return True
        except ValueError:
            return False
