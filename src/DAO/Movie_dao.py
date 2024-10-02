from typing import List, Optional

from DAO.db_connection import DBConnection
from Model.Movie import Movie


# A Faire: (valentine)
class Movie_dao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def insert(self, new_movie: Movie):
        """
        Adds a movie into the database.

        Parameters:
        -----------
        new_movie : Movie
            A new movie to add to the database

        """
        # if new_movie.id already exists do an error.
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO movie (
                               )
                    VALUES (
                               )
                               """)
            self.db_connection.connection.commit()
            print("Insersion successful : MovieMaker added.")
        except Exception as e:
            print("Insersion error : ", str(e))

    # structure prise du TP
    def find_Movie_by_id(self, id: int) -> Movie:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT *                                  "
                        "  FROM tp.attack a                     "
                        f"  WHERE a.id_attack = {id}"
                    )
                    res = cursor.fetchone()
                except Exception as e:
                    print(f" Erreur : {e}")
                    return None
                return res


"""
tout ceci est inclu si on utilisedes with
conn.commit()
cursor.close()
conn.close()

Pour récupérer des élement
cursor.fetchone()
cursor.fetchall()
cursor.fetchmany(size)

Pour modifier
cursor.execute()
"""
