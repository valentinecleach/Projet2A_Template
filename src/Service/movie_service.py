from src.DAO.movie_dao import Movie_dao
from src.TMDB.movie_tmdb import MovieTMDB 
from src.Model.movie import Movie
from typing import List, Dict

class MovieService:
    def __init__(self, movie_db: None):
        self.movie_dao = Movie_dao()
        self.movie_tmdb = MovieTMDB()

    def get_movie_by_id(self, movie_id : int, test) -> Movie | None:
        """find movie by id """
        movie = self.movie_dao.get_by_id(movie_id, test)
        if movie :
            return movie
        else :
            movie_from_tmdb = self.movie_tmdb.get_movie_by_id(id)
            if movie_from_tmdb:
                self.movie_dao.insert(movie_from_tmdb, test)
                return movie_from_tmdb
            else :
                print(f"No Movie found with id :{movie_id}.")
                return None

    def create_movies(self, known_for_data : List[Dict]) -> List[Movie]:
        """
        Transforms a list of dictionaries into a list of Movie objects.

        Parameters:
        known_for_data 
            List[Dict]: A list of dictionaries containing movie information.

        Returns:
        List[Movie]: A list of Movie objects.
        """
        list_movies = []
        for item in known_for_data:
            movie = Movie(**item)
            list_movies.append(movie)
        return list_movies



#################################################################################################

    def find_by_id(self, movie_id: int) -> Movie:
        """Find movie by id"""
        return Movie(id=1, original_title="A Clockwork Orange")
        # return self.movie_db.get_by_id(movie_id)

    def find_by_title(self, movie_title: str) -> Movie:
        """Find movie by title"""
        pass

    def view_comments(self, movie: Movie) -> ...:
        """View the comments of a movie"""
        pass

#    def filter_by_genre(self, genre: Genre) -> ...: 
#       """Filter movies by their genre"""
#        pass

    def filter_by_popularity(self) -> list[Movie]:
        """Filters the movie by the popularity"""
        pass
