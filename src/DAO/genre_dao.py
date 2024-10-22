from typing import Dict, List, Optional
from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.Model.genre import Genre

class GenreDao(metaclass=Singleton):
    def __init__(self):
        # create a DB connection object
        self.db_connection = DBConnection()
        # Create tables if don't exist
        self.db_connection.create_tables()

    def insert(self, new_genre): 
        try:
            """
            Adds a Genre into the database.

            Parameters:
            -----------
            new_genre : Genre
                The Genre to add in the schema

            """
            # Connexion
            with self.db_connection.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    # SQL resquest
                    cursor.execute(
                        "SELECT id_genre FROM genre WHERE id_genre = %s",
                        (new_genre.id,)
                    )
                    genre_exists = cursor.fetchone()

                    if genre_exists is None:
                        cursor.execute(
                            """
                            INSERT INTO Genre (id_genre ,
                                                name_genre)
                            VALUES (%s, %s)
                            """,
                            (
                                new_genre.id,
                                new_genre.name
                            ),
                        )
                    connection.commit()
                    print("Insertion successful : Genre added.")
        except Exception as e:
            print("Insertion error : ", str(e))

# works : add a new genre in the schema 
#mon_objet = GenreDao()
#mon_objet.insert(Genre(id =  28, name = "Action"))