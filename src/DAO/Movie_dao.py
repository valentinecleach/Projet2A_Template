from typing import List, Optional, Dict
from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.Model.movie import Movie


# A Faire: (valentine)
class MovieDAO(metaclass=Singleton):
    def insert(self, new_movie: Movie, test: bool):
        try:
            """
            Adds a movie into the database.

            Parameters:
            -----------
            new_movie : Movie
                A new movie to add to the database

            """
            # if new_movie.id already exists do an error.
            # Connexion
            with DBConnection(test).connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    # SQL resquest
                    cursor.execute(
                        
                        """
                        INSERT INTO Movie (id ,
                                            title ,
                                            belongs_to_collection ,
                                            budget,
                                            genres ,
                                            origin_country ,
                                            original_language,
                                            original_title,
                                            overview,
                                            popularity,
                                            release_date,
                                            revenue,
                                            runtime,
                                            vote_average,
                                            vote_count,
                                            adult)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            new_movie.id ,
                            new_movie.title ,
                            new_movie.belongs_to_collection ,
                            new_movie.budget,
                            new_movie.genres ,
                            new_movie.origin_country ,
                            new_movie.original_language,
                            new_movie.original_title,
                            new_movie.overview,
                            new_movie.popularity,
                            new_movie.release_date,
                            new_movie.revenue,
                            new_movie.runtime,
                            new_movie.vote_average,
                            new_movie.vote_count,
                            new_movie.adult
                        ),
                    )
                    # tagline? status?)
                # Fetching the result
                res = cursor.fetchone()

            # if we have a result
            if res:
                pass
                # what_we_returne =
                print("Insertion successful : Movie added.")
        except Exception as e:
            print("Insertion error : ", str(e))
            # return None #what_we_return

    def update(self, movie: Movie, test: bool):
        try:
            with DBConnection(test).connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE Movie
                    SET adult = %s, genre.id = %s , original_title = %s
                    , overview = %s,popularity = %s, release_date = %s,
                    title = %s, vote_average = %s,vote = %s
                    WHERE id_movie = %s;
                """,
                    (
                        movie.adult,
                        movie.genre.id,
                        movie.original_title,
                        movie.overview,
                        movie.popularity,
                        movie.release_date,
                        movie.title,
                        movie.vote_average,
                        movie.vote,
                    ),
                )
                self.db_connection.connection.commit()
                print("Update successful : movie updated.")
        except Exception as e:
            print("Update error : ", str(e))

    def delete(self, id_movie: int, test: bool):
        try:
            with DBConnection(test).connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM Movie
                    WHERE id_movie = %s;
                """,
                    (id_movie,),
                )

                self.db_connection.connection.commit()
                print("Deletion successful : Movie deleted.")
        except Exception as e:
            print("Delete error : ", str(e))

    # structure prise du TP
    def get_by_id(self, id_movie: int, test: bool) -> Movie:
        try:
            with DBConnection(test).connection as connection:
                # Creation of a cursor for the request
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM Movie
                        WHERE id = %s;
                        """,
                        (id,),
                    )
                    result = cursor.fetchone()
                if result:
                    return Movie(**result)
                else:
                    print("NO Movie with this id.")
                    return None
        except Exception as e:
            print("Error during recovery by id : ", str(e))
            return None

    def get_by_name(self, name: str, test: bool) -> List[Movie] | None:
        try:
            with DBConnection(test).connection.cursor() as cursor:
                cursor.execute(
                    """
                        SELECT * FROM Movie
                        WHERE name ILIKE %s;
                    """,
                    (f"%{name}%",),
                )  # -- ILIKE for case-insensitive searching
                results = cursor.fetchall()
                return [Movie(**row) for row in results] if results else []
        except Exception as e:
            print("Error during recovery by name : ", str(e))
            return None



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
