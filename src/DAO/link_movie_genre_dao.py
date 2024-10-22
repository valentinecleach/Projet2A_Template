from typing import Dict, List, Optional
from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton

class LinkMovieGenreDAO(metaclass=Singleton):

    def __init__(self):
        # create a DB connection object
        self.db_connection = DBConnection()
        # Create tables if don't exist
        self.db_connection.create_tables()
    
    def insert(self, id_movie, id_genre): 
        try:
            
            # Connexion
            with self.db_connection.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    # SQL resquest
                    cursor.execute(
                        """
                        SELECT COUNT(*) FROM link_movie_genre 
                        WHERE id_movie = %s AND id_genre = %s
                        """,
                        (id_movie, id_genre)
                    )
                    link_exists = cursor.fetchone()[0] > 0

                    if link_exists is None:
                        cursor.execute(
                        """
                        INSERT INTO link_movie_genre (id_movie, id_genre)
                        VALUES (%s, %s)
                        """,
                        (id_movie, id_genre)  # Assurez-vous que genre.id_genre existe
                    )
                    connection.commit()
                    print("Insertion successful : Link Movie Genre added.")
        except Exception as e:
            print("Insertion error : ", str(e))