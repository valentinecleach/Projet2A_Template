from typing import Dict, List

from src.DAO.movie_dao import MovieDAO
from src.Model.movie import Movie
from src.TMDB.movie_tmdb import MovieTMDB
from src.DAO.db_connection import DBConnector

class MovieService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.movie_dao = MovieDAO(db_connection)
        self.movie_tmdb = MovieTMDB()

    def get_movie_by_id(self, movie_id: int) -> Movie | None:
        """find movie by id"""
        movie = self.movie_dao.get_by_id(movie_id)
        if movie:
            print("Movie get from database")
            return movie
        else:
            movie_from_tmdb = self.movie_tmdb.get_movie_by_id(movie_id)
            if movie_from_tmdb:
                self.movie_dao.insert(movie_from_tmdb)
                print(f"Movie with id {movie_id} get from TMDB and inserted")
                return movie_from_tmdb
            else:
                print(f"No Movie found with id :{movie_id}.")
                return None


    def get_movie_by_title(self, movie_title : str) -> Movie | None :
        """find movie by title"""
        movie = self.movie_dao.get_by_title(movie_title)
        if movie:
            print("Movie get from database")
            return movie
        else:
            movie_from_tmdb = self.movie_tmdb.get_movies_by_title(movie_title)
            if movie_from_tmdb:
                for movie in movie_from_tmdb:
                    self.movie_dao.insert(movie)
                print("Movies added in database")
            else:
                print(f"No Movie found with id :{movie_id}.")
                return None


    def create_movies(self, known_for_data: List[Dict]) -> List[Movie]:
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
            id_movie = item['id']
            movie = self.get_movie_by_id(id_movie)
            if movie:
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

# db_connection = DBConnector()
# my_object = MovieService(db_connection)
# print(my_object.get_movie_by_id(1252415))
# #print(my_object.get_movie_by_title('Avatar'))


