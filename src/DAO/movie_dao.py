from typing import Dict, List, Optional
from datetime import date

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.genre_dao import GenreDao
from src.DAO.link_movie_genre_dao import LinkMovieGenreDAO
from src.DAO.link_movie_movie_collection_dao import LinkMovieMovieCollectionDAO
from src.DAO.movie_collection_dao import MovieCollectionDao
from src.DAO.singleton import Singleton

from src.Model.movie import Movie


class MovieDAO(metaclass=Singleton):
    """MovieDao is DAO for managing movies in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    genre_dao : GenreDao
        A DAO object used for operations related to genre.
    movie_collection_dao : MovieCollectionDao
        A DAO object used for operations related to movie collections.
    link_movie_genre_dao : LinkMovieGenreDAO
        A DAO object used to create links between movies and their genres.
    link_movie_movie_collection_dao : LinkMovieMovieCollectionDAO
        A DAO object used to create links between movies and movie collections.
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor."""
        self.db_connection = db_connection
        self.genre_dao = GenreDao(db_connection)
        self.movie_collection_dao = MovieCollectionDao(db_connection)
        self.link_movie_genre_dao = LinkMovieGenreDAO(db_connection)
        self.link_movie_movie_collection_dao = LinkMovieMovieCollectionDAO(
            db_connection
        )

    def insert(self, new_movie: Movie):
        """
        Adds a movie into the database along with its genres and collections.

        Parameters:
        -----------
        new_movie : Movie
            A new movie to add to the database.
        """
        try:
            query = """
                SELECT COUNT(*)
                FROM movie
                WHERE id_movie = %s;
            """
            result = self.db_connection.sql_query(query, (new_movie.id_movie,), return_type = "one")
            movie_exist = result["count"] > 0  # True si film, False sinon

            if not movie_exist:
                print(f"Inserting movie: {new_movie.title}")
                insert_query = """
                            INSERT INTO movie (id_movie, title, budget, origin_country, 
                                            original_language, original_title, overview, 
                                            popularity, release_date, revenue, runtime, 
                                            vote_average, vote_count, adult)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                    %s, %s, %s, %s)
                            """
                values = (
                    new_movie.id_movie,
                    new_movie.title,
                    (new_movie.budget if new_movie.budget is not None else None),
                    (new_movie.origin_country if new_movie.origin_country is not None else None),
                    (new_movie.original_language if new_movie.original_language is not None else None),
                    (new_movie.original_title if new_movie.original_title is not None else None),
                    (new_movie.overview if new_movie.overview is not None else None),
                    (new_movie.popularity if new_movie.popularity is not None else None),
                    (new_movie.release_date if new_movie.release_date is not None else None),
                    (new_movie.revenue if new_movie.revenue is not None else None),
                    (new_movie.runtime if new_movie.runtime is not None else None),
                    (new_movie.vote_average if new_movie.vote_average is not None else None),
                    (new_movie.vote_count if new_movie.vote_count is not None else None),
                    new_movie.adult,
                )
                self.db_connection.sql_query(insert_query, values)
                print(f"Insertion movie successful: {new_movie.title}")

            # Insertion des genres
            if new_movie.genres:
                print("inserting new movie genre")
                for genre in new_movie.genres:
                    self.genre_dao.insert(new_genre=genre)
                    self.link_movie_genre_dao.insert(new_movie.id_movie, genre.id)

            # Insertion de la collection si elle existe
            if new_movie.belongs_to_collection:
                print("insertion new movie collection")
                for collection in new_movie.belongs_to_collection:
                    self.movie_collection_dao.insert(collection)
                    self.link_movie_movie_collection_dao.insert(
                        new_movie.id_movie, collection.id
                    )
            print("insertion successful : movie added")
        except Exception as e:
            print("Insertion error: ", str(e))

    def get_by_id(self, id_movie: int) -> Movie:
        """Gets a movie from the database with it's ID.

        Parameters
        ----------
        id_movie: int
            The ID of the movie to select.

        Returns
        -------
        Movie
            The movie that corresponds to the ID given.
        """
        try:
            # Retrieves the movie
            query = """
                SELECT * FROM movie
                WHERE id_movie = %s;
            """
            result = self.db_connection.sql_query(query, (id_movie,), return_type="one")

            if result:
                movie_data = dict(result)

                # Retrieves the genres associated to the movie
                try:
                    genres_query = """
                        SELECT g.id_genre, g.name_genre
                        FROM link_movie_genre l
                        JOIN Genre g ON l.id_genre = g.id_genre
                        WHERE l.id_movie = %s;
                    """
                    genres_result = self.db_connection.sql_query(
                        genres_query, (id_movie,), return_type="all"
                    )
                    movie_data["genres"] = [
                    {"id": genre["id_genre"], "name": genre["name_genre"]}
                    for genre in genres_result
                    ]
                except Exception as e:
                    print("Error during recovery associated genre: ", str(e))
                    

                # Retrieves the collections of movies associated to the movie.
                try:
                    collections_query = """
                        SELECT mc.id_movie_collection, mc.name_movie_collection
                        FROM link_movie_movie_collection lm
                        JOIN Movie_Collection mc ON lm.id_movie_collection = mc.id_movie_collection
                        WHERE lm.id_movie = %s;
                    """
                    collections_result = self.db_connection.sql_query(
                        collections_query, (id_movie,), return_type="all"
                    )
                    movie_data["belongs_to_collection"] = [
                    {
                        "id": collection["id_movie_collection"],
                        "name": collection["name_movie_collection"],
                    }
                    for collection in collections_result
                    ]
                except Exception as e:
                    print("Error during recovery associated collection: ", str(e))             
                return Movie(**movie_data)
            else:
                print("No movie found with this ID in the database.")
                return None

        except Exception as e:
            print("Error during get by id: ", str(e))
            return None

    def update(self, movie: Movie):
        """Updates a movies information in the database.

        Parameters
        ----------
        movie: Movie
            The new information of the movie.

        """ 
        try:
            query = """
                    UPDATE Movie
                    SET revenue = %s, popularity = %s, vote_average = %s, vote_count = %s
                    WHERE id_movie = %s;
                """
            values = (
                        movie.revenue,
                        movie.popularity,
                        movie.vote_average,
                        movie.vote_count,
                        movie.id_movie
                    )
            self.db_connection.sql_query(query, values)
            print("Update successful : movie updated.")
        except Exception as e:
            print("Update error : ", str(e))

    def delete(self, id_movie: int):
        """Deletes a movie from the database using it's ID.

        Parameters
        ----------
        id_movie: int
            The ID of the movie that will get deleted.
        """ 
        try:
            with self.self.db_connection.connection.cursor() as cursor:
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


    def get_by_title(self, title: str) -> List[Movie] | None:
        """Selects a list of movies from the database using a movie title.

        Parameters
        ----------
        title: str
            The title of a movie.

        Returns
        -------
        List[Movie]
            A list of movies with a given title or a similar title.
        """ 
        try:
            query = """
                SELECT id_movie FROM movie
                WHERE title ILIKE %s;
            """
            results = self.db_connection.sql_query(
                query, (f"%{title}%",), return_type="all"
            )

            if results:  # Verifying that resultats have been found
                movies = []
                for result in results:
                    # Retrieves every film using their ID
                    movie = self.get_by_id(result["id_movie"])
                    if movie:
                        movies.append(movie)
                return movies
            else:
                print("No movie with this title in the database.")
                return None
        except Exception as e:
            print("Error during recovery by title:", str(e))
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
