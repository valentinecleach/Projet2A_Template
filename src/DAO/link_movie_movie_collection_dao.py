from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton


class LinkMovieMovieCollectionDAO(metaclass=Singleton):

    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def insert(self, id_movie: int, id_movie_collection: int):
        try:
            # Vérification de l'existence du lien
            query = """
                SELECT COUNT(*) FROM link_movie_movie_collection 
                WHERE id_movie = %s AND id_movie_collection = %s;
            """
            result = self.db_connection.sql_query(query, (id_movie, id_movie_collection,), return_type="one")
            link_exists = result["count"] > 0 if result else False

            if not link_exists:
                print("Inserting link between movie and movie collection.")
                insert_query = """
                    INSERT INTO link_movie_movie_collection (id_movie, id_movie_collection)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (id_movie, id_movie_collection,))
                print("Insertion successful: Link Movie Movie Collection added.")
            else:
                print("Link already exists.")

        except Exception as e:
            print("Insertion error: ", str(e))
