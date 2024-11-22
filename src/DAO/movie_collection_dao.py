from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.movie_collection import MovieCollection


class MovieCollectionDao(metaclass=Singleton):
    """MovieCollectionDao is DAO for managing collections of movies in the
    database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database
    """

    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection

    def insert(self, new_movie_collection):
        """
        Adds a Movie Collection into the database.

        Parameters:
        -----------
        new_movie_collection : MovieCollection
            The Movie Collection to add in the schema.
        """
        try:
            # Verifying the existence of the collection
            query = "SELECT id_movie_collection FROM movie_collection WHERE id_movie_collection = %s;"
            movie_collection_exists = self.db_connection.sql_query(
                query, (new_movie_collection.id,), return_type="one"
            )

            if movie_collection_exists is None:
                insert_query = """
                    INSERT INTO movie_collection (id_movie_collection, name_movie_collection)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(
                    insert_query,
                    (
                        new_movie_collection.id,
                        new_movie_collection.name,
                    ),
                )
                print("Insertion successful: Movie Collection added.")
            else:
                print(
                    f"Movie Collection with id {new_movie_collection.id} already exists."
                )

        except Exception as e:
            print("Insertion error: ", str(e))

    
    def get_movie_collection_by_id(
        self,
        id: int,
    ) -> MovieCollection:
        """Fetches a collection of movies by it's ID.

        Parameters
        ----------
        id : int
            A ID of a movie collection

        Returns
        -------
        MovieCollection | None
            The movie collection that corresponds to the ID.
            If the ID doesn't exist, then the function will return None.
        """
        try:
            query = "SELECT * FROM  movie _collection WHERE id = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id))
                    res = cursor.fetchone()
            if res:
                return MovieCollection(res)
            else:
                return None
        except Exception:
            return None

    
    def get_all(
        self,
        limit: int = 10,
    ) -> List[MovieCollection]:
        """Fetches all collections of movies.

        Parameters
        ----------
        limit : int
            A number of the maximum of movie collections to return

        Returns
        -------
        List[MovieCollection] | None
            A list of movie collections.
            If no movie collections are found, then the function will return None.
        """
        try:
            query = f"SELECT * FROM  movie_collection LIMIT {max(limit, 0)}"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                    )
                    results = cursor.fetchall()
            if results:
                coll = [MovieCollection(res) for res in results]
                return coll
            else:
                return None
        except Exception:
            return None

    
    def delete(self, id):
        """Deletes a collection of movies.

        Parameters
        ----------
        id : int
            The ID of the movie collection to delete.
        """
        try:
            query = "DELETE FROM  movie_collection WHERE id = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id),
                    )
                    connection.commit()
                    print("Record deleted successfully from movie collection.")
        except Exception as e:
            print(f"Error while deleting from movie collection: {e}")
            return None