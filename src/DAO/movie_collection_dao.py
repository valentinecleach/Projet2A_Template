from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.Model.movie_collection import MovieCollection


class MovieCollectionDao(metaclass=Singleton):
    def __init__(self):
        # create a DB connection object
        self.db_connection = DBConnection()
        # Create tables if don't exist
        self.db_connection.create_tables()
    
    def insert(self, new_movie_collection):
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
                        """
                        INSERT INTO movie_collection (id_movie_collection ,
                                            name_movie_collection)
                        VALUES (%s, %s)
                        """,
                        (
                            new_movie_collection.id,
                            new_movie_collection.name
                        ),
                    )
                connection.commit()

            print("Insertion successful : Movie Colelction added.")
        except Exception as e:
            print("Insertion error : ", str(e))


#######################################################################################
    # READ (Fetch a specific user's comment)
    def get_movie_collection_by_id(
        self,
        id: int,
    ) -> MovieCollection:

        try:
            query = "SELECT * FROM  movie _collection WHERE id = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id))
                    res = cursor.fetchone()
            if res:
                return MovieCollection(res)
            else:
                return None
        except Exception:
            return None


    # READ (Fetch all comments of a specific movie)
    def get_all(
        self,
        limit: int = 10,
    ) -> List[MovieCollection]:

        try:
            query = f"SELECT * FROM  movie_collection LIMIT {max(limit, 0)}"
            with DBConnection().connection as connection:
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

    # DELETE / SUPPRIME
    def delete(self, id):
        try:
            query = "DELETE FROM  movie_collection WHERE id = %s"
            with DBConnection().connection as connection:
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

# works : add a new Movie Collecction in the schema 
mon_objet = MovieCollectionDao()
mon_objet.insert(MovieCollection(id = 87096, name = 'Avatar Collection'))