from datetime import datetime
from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.tables_creation import TablesCreation


class UserMovieCollectionDao(metaclass=Singleton):
    """UserMovieCollectionDao is DAO for managing collection of movies made by users in the database.
    They can represent a collection of favorite movies.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    tables_creation :

    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        # Creates tables if they don't already exist
        self.tables_creation = TablesCreation(db_connection)

    def insert(self, id_user: int, id_movie: int):
        """
        Adds a film to the users collection of movies.

        Parameters
        -----------
        id_user : int
            The ID of a user.
        id_movie : int
            The ID of a movie to add to the collection.
        """
        date = datetime.now()
        try:
            # Connection
            with self.db_connection.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    # SQL request
                    cursor.execute(
                        "SELECT id_movie FROM user_movie_collection WHERE id_user = %s",
                        (id_user,),
                    )
                    movie_exists = cursor.fetchone()

                    if movie_exists is None:
                        cursor.execute(
                            """
                            INSERT INTO user_movie_collection (id_user, id_movie,date)
                            VALUES (%s, %s)
                            """,
                            (id_user, id_movie, date),
                        )
                        connection.commit()
                        print("Insertion successful : movie added.")
                    else:
                        print(
                            f"movie with id {id_movie} already exists in {id_user} collection."
                        )
        except Exception as e:
            print("Insertion error : ", str(e))

    def get_all_collection(
        self, id_user: int, limit: int = 10, offset: int = 0
    ) -> list | None:
        """Gets all movies from a users movie collection within a certain limit.

        Parameters
        ----------
        id_user : int
            The ID of a user.
        limit : int 
            The maximum number of movies to get. By default this is 10
        offset : int
            The amount of movies to skip before starting to return movies.
            By default, the offset is 0.

        Returns
        -------
        list[Movie] | None
            The list of movies. Returns None if there was an error fetching the movies.
        """
        try:
            query = f"SELECT * FROM user_movie_collection WHERE id_user = %s LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        return results

    def delete(self, id_user: int, id_movie: int):
        """Deletes a movie from a users movie collection.

        Parameters
        ----------
        id_user : int
            The ID of a user.
        id_movie : int
            The ID of a movie to delete
        """
        try:
            query = (
                "DELETE FROM user_movie_collection WHERE id_user = %s and id_movie = %s"
            )
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_movie,
                        ),
                    )
                    connection.commit()
                    print("Record deleted successfully FROM user_movie_collection.")
        except Exception as e:
            print(f"Error while deleting FROM user_movie_collection: {e}")
            self.db_connection.connection.rollback()
            return None
