from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.genre import Genre


class GenreDao(metaclass=Singleton):
    """
    GenreDAO is DAO for managing genres in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database
    """

    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection

    def insert(self, new_genre: Genre):
        """
        Adds a new genre to the database.

        Parameters:
        -----------
        new_genre : Genre
            The genre to add.
        """
        try:
            # Verifying the existence of the genre
            query = "SELECT id_genre FROM genre WHERE id_genre = %s;"
            genre_exists = self.db_connection.sql_query(
                query, (new_genre.id,), return_type="one"
            )

            if genre_exists is None:
                insert_query = """
                    INSERT INTO Genre (id_genre, name_genre)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(
                    insert_query,
                    (
                        new_genre.id,
                        new_genre.name,
                    ),
                )
                print("Insertion successful: Genre added.")
            else:
                print(f"Genre with id {new_genre.id} already exists.")

        except Exception as e:
            print("Insertion error: ", str(e))
