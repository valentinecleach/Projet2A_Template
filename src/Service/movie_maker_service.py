# src/Service/MovieMakerService.py
from src.DAO.movie_maker_dao import MovieMakerDAO
from src.TMDB.movie_maker_tmdb import MovieMakerTMDB
from src.Model.movie_maker import MovieMaker


class MovieMakerService:
    def __init__(self):
        self.movie_maker_dao = MovieMakerDAO()
        self.movie_maker_tmdb = MovieMakerTMDB()

    def get_movie_maker_by_name(self, name: str, test) -> list[MovieMaker] | None:
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
        movie_makers = self.movie_maker_dao.get_by_name(name, test)

        if movie_makers:
            return movie_makers # a list of 1 or many MovieMakers

        # If not in our database, we look for the MovieMaker in the TMDB api.
        movie_maker_from_tmdb = self.movie_maker_tmdb.get_movie_maker_by_name_or_by_id(name)
        
        if movie_maker_from_tmdb:
            for data in movie_maker_from_tmdb:
                self.movie_maker_dao.insert(data, test)
            return movie_maker_from_tmdb

        # Si rien n'est trouvé
        print(f"No MovieMaker found with name: {name}.")
        return None