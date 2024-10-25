from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.DAO.tables_creation import TablesCreation


class LinkMovieMovieCollectionDAO(metaclass=Singleton):

    def __init__(self, db_connection: DBConnection):
        # create a DB connection object
        self.db_connection = db_connection
        # Create tables if don't exist
        self.tables_creation = TablesCreation(db_connection)

    def insert(self, id_movie, id_movie_collection):
        try:

            # Connexion
            with self.db_connection.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    # SQL resquest
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM link_movie_movie_collection 
                        WHERE id_movie = %s AND id_movie_collection = %s
                        """,
                        (id_movie, id_movie_collection),
                    )
                    result = cursor.fetchone()
                    link_exists = result["count"] > 0

                    if not link_exists:
                        cursor.execute(
                            """
                        INSERT INTO link_movie_movie_collection (id_movie, id_movie_collection)
                        VALUES (%s, %s)
                        """,
                            (id_movie, id_movie_collection),
                        )
                    connection.commit()
                    print("Insertion successful : Link Movie Movie Collection added.")
        except Exception as e:
            print("Insertion error : ", str(e))
