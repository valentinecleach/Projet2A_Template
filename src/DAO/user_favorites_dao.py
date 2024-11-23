from datetime import datetime

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.movie_dao import MovieDAO

class UserFavoriteDao(metaclass=Singleton):
    """UserFavoriteDao is DAO for managing a users favorite movies in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection

    def insert(self, id_user: int, id_movie: int):
        """Inserts a relationship between a user and a favorite movie into user_movie_collection if it doesn't already exist.
        
        Parameters
        ----------
        id_user: int 
            The ID of the user.
        id_movie : int
            The ID of the movie.
        """
        try:
            # Verifying the existence of a link
            query = """
                SELECT COUNT(*) as count FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (id_user, id_movie),
                return_type="one",
            )

            favorite_exists = result["count"] > 0 if result else False

            if not favorite_exists:
                print("Inserting favorite relationship.")
                insert_query = """
                    INSERT INTO user_movie_collection (id_user, id_movie, date)
                    VALUES (%s, %s, %s);
                """
                the_date = datetime.now().date()
                values = (id_user, id_movie, the_date)
                self.db_connection.sql_query(insert_query, values)
                print("Insertion successful: Favorite relationship added.")
            else:
                print("Favorite relationship already exists, no insertion performed.")
        except Exception as e:
            print("Insertion error:", str(e))

    def get_favorites(self, id_user: int) -> List[int]|None:
        """Retrieves the list of a users favorite films
        
        Parameters
        ----------
        id_user : the ID of a user.

        Returns
        -------
        list[int]
            The list of the ID of movies that are the users favorites. 
            If no movies can be found, the method returns None.
        """
        try:
            select_query = """
                SELECT id_movie, date FROM user_movie_collection
                WHERE id_user = %s
                ORDER BY date DESC;
            """
            results = self.db_connection.sql_query(
                select_query, (id_user,), return_type="all"
            )
            if results:
                favorites = [result['id_movie'] for result in results]
                return favorites 
            else:
                return None
        except Exception as e:
            print("Retrieval error:", str(e))
            return []

    def remove(self, id_user: int, id_movie: int):
        """Removes a movie from the favorites of a user.
        
        Parameters
        ----------
        id_user : int
            The ID of a user.
        id_movie : int
            The ID of a movie.
        """
        try:
            delete_query = """
                DELETE FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """
            self.db_connection.sql_query(delete_query, (id_user, id_movie))
            print("Deletion successful: Movie removed from favorites.")
        except Exception as e:
            print("Deletion error:", str(e))
