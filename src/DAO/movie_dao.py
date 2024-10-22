from typing import Dict, List, Optional
from psycopg2.extras import DictCursor
# DAO
from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.DAO.genre_dao import GenreDao
from src.DAO.movie_collection_dao import MovieCollectionDao
from src.DAO.link_movie_genre_dao import LinkMovieGenreDAO
from src.DAO.link_movie_movie_collection_dao import LinkMovieMovieCollectionDAO
# Model
from src.Model.movie import Movie


# A Faire: (valentine)
class MovieDAO(metaclass=Singleton):
    def __init__(self):
        # create a DB connection object
        self.db_connection = DBConnection()
        # Create tables if don't exist
        self.db_connection.create_tables()
        self.genre_dao = GenreDao()
        self.movie_collection_dao = MovieCollectionDao()
        self.link_movie_genre_dao = LinkMovieGenreDAO()
        self.link_movie_movie_collection_dao = LinkMovieMovieCollectionDAO()

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
                        SELECT COUNT(*)
                        FROM movie
                        WHERE id_movie = %s;
                        """,
                        (new_movie.id_movie,)
                    )
                    result = cursor.fetchone()
                    movie_exist = result['count'] > 0 # True si film, False sinon
                    if not movie_exist:
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
                        # Commit des changements
                        connection.commit()
                    print(f"Insertion movie successful: {new_movie.title}")

            # Insertion des genres
            if new_movie.genres:
                print('inserting new movie genre')
                for genre in new_movie.genres:
                    self.genre_dao.insert(new_genre = genre)
                    self.link_movie_genre_dao.insert(new_movie.id_movie,genre.id)

            # Insertion de la collection si elle existe
            if new_movie.belongs_to_collection:
                print('insertion new movie collection')
                for collection in new_movie.belongs_to_collection:
                    self.movie_collection_dao.insert(collection)
                    self.link_movie_movie_collection_dao.insert(new_movie.id_movie, collection.id)
            print('insertion successful : movie added' )    
        except Exception as e:
            print("Insertion error: ", str(e))

    def get_by_id(self, id_movie: int) -> Movie:
        try:
            with self.db_connection.connection as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    # Récupérer le film
                    cursor.execute(
                        """
                        SELECT * FROM Movie
                        WHERE id_movie = %s;
                        """,
                        (id_movie,),
                    )
                    result = cursor.fetchone()
                if result:
                    movie_data = dict(result)
                    print(movie_data.keys())
                    cursor.execute(
                        """
                        SELECT g.id_genre, g.name_genre
                        FROM link_movie_genre l
                        JOIN Genre g ON l.id_genre = g.id_genre
                        WHERE l.id_movie = %s;
                        """,
                        (id_movie,)
                        )
                    genres = cursor.fetchall()

                    # Récupérer les collections associées
                    cursor.execute(
                        """
                        SELECT mc.id_movie_collection, mc.name_collection
                        FROM link_movie_movie_collection lm
                        JOIN Movie_Collection mc ON lm.id_movie_collection = mc.id_movie_collection
                        WHERE lm.id_movie = %s;
                        """,
                        (id_movie,)
                    )
                    collections = cursor.fetchall()     

                    movie_data['genres'] = [dict(genre) for genre in genres] 
                    movie_data['belongs_to_collection'] = [dict(collection) for collection in collections] 

                    return(Movie(**movie_data))
                else:
                    print("No movie with this ID.")
                    return None           
        except Exception as e:
            print("Error during recovery by id : ", str(e))
            return None

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
