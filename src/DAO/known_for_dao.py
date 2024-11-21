from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton


class KnownForDao(metaclass=Singleton):
    """
    KnownForDao is DAO for managing links between people in the film industry
    and their films in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database
    """

    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection

    def insert(self, id_movie: int, id_movie_maker: int):
        """Inserts a link between a movie maker and their film.

        Parameters
        ----------
        id_movie : int
            The ID of a movie.
        id_movie_maker : int
            The ID of a movie maker.
        """
        try:
            # Verifying the existance of the link
            query = """
                SELECT COUNT(*) FROM knownfor
                WHERE id_movie = %s AND id_movie_maker = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (
                    id_movie,
                    id_movie_maker,
                ),
                return_type="one",
            )
            link_exists = result["count"] > 0 if result else False

            if not link_exists:
                print("Inserting known for link between movie and movie maker.")
                insert_query = """
                    INSERT INTO knownfor (id_movie, id_movie_maker)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(
                    insert_query,
                    (
                        id_movie,
                        id_movie_maker,
                    ),
                )
                print("Insertion successful: Known for linked added.")
            else:
                print("Link already exists.")

        except Exception as e:
            print("Insertion error: ", str(e))
