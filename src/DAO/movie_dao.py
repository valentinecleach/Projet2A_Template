from typing import Dict, List, Optional
from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.Model.movie import Movie


# A Faire: (valentine)
class MovieDAO(metaclass=Singleton):
    def __init__(self):
        # create a DB connection object
        self.db_connection = DBConnection()
        # Create tables if don't exist
        self.db_connection.create_tables()
    def insert(self, new_movie: Movie):
        try:
            """
            Adds a movie into the database along with its genres and collections.

            Parameters:
            -----------
            new_movie : Movie
                A new movie to add to the database
            """
            # Connexion
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    print(f"Inserting movie: {new_movie.title}")
                    cursor.execute(
                        """
                        INSERT INTO movie (id_movie, title, budget, origin_country, 
                                        original_language, original_title, overview, 
                                        popularity, release_date, revenue, runtime, 
                                        vote_average, vote_count, adult)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s)
                        """,
                        (
                            new_movie.id_movie,
                            new_movie.title,
                            new_movie.budget if new_movie.budget is not None else None,
                            new_movie.origin_country if new_movie.origin_country is not None else None,
                            new_movie.original_language,
                            new_movie.original_title,
                            new_movie.overview,
                            new_movie.popularity,
                            new_movie.release_date,
                            new_movie.revenue if new_movie.revenue is not None else None,
                            new_movie.runtime if new_movie.runtime is not None else None,  # Gérer runtime
                            new_movie.vote_average,
                            new_movie.vote_count,
                            new_movie.adult,
                        ),
                    )
                    print(f"Insertion movie successful: {new_movie.title}")

                    # Insertion des genres
                    if new_movie.genres:
                        for genre in new_movie.genres:
                            cursor.execute(
                                """
                                INSERT INTO genre (id_genre, name_genre)
                                VALUES (%s, %s)
                                """,
                                (genre.id, genre.name)  # Assurez-vous que genre.id_genre existe
                            )
                            cursor.execute(
                                """
                                INSERT INTO link_movie_genre (id_movie, id_genre)
                                VALUES (%s, %s)
                                """,
                                (new_movie.id_movie, genre.id)  # Assurez-vous que genre.id_genre existe
                            )

                    # Insertion de la collection si elle existe
                    if new_movie.belongs_to_collection:
                        collection = new_movie.belongs_to_collection
                        cursor.execute(
                            """
                            INSERT INTO movie_collection (id_movie_collection, name_movie_collection)
                            VALUES (%s, %s)
                            """,
                            (collection.id, collection.name)
                        )

                        # Lien entre Movie et Movie Collection
                        cursor.execute(
                            """
                            INSERT INTO link_movie_movie_collection (id_movie, id_movie_collection)
                            VALUES (%s, %s)
                            """,
                            (new_movie.id_movie, collection.id)
                        )

                # Commit des changements
                connection.commit()
                print("Insertion successful: Movie added.")
        except Exception as e:
            print("Insertion error: ", str(e))


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
