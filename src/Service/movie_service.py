from src.DAO.movie_dao import MovieDAO
from src.TMDB.movie_tmdb import MovieTMDB
from src.Model.movie import Movie


class MovieService:
    def __init__(self, movie_db: None):
        self.movie_dao = MovieDAO()
        self.movie_tmdb = MovieTMDB()

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

    def filter_by_genre(self, genre: Genre) -> ...: 
        """Filter movies by their genre"""
        pass

    def filter_by_popularity(self) -> list[Movie]:
        """Filters the movie by the popularity"""
        pass
