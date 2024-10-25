from typing import Dict, List, Optional
from datetime import datetime
from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.DAO.tables_creation import TablesCreation


class UserMovieCollectionDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnection):
        # create a DB connection object
        self.db_connection = db_connection
        # Créer des tables si elles n'existent pas
        self.tables_creation = TablesCreation(db_connection)

    def insert(self, id_user : int, id_movie: int):
        date = datetime.now()
        try:
            """
            Ajoute un film dans la base de données.

            Paramètres:
            -----------
            """
            # Connexion
            with self.db_connection.connection as connection:
                # Création d'un curseur pour la requête
                with connection.cursor() as cursor:
                    # SQL resquest
                    cursor.execute(
                        "SELECT id_movie FROM user_movie_collection WHERE id_user = %s",
                        (id_user,),
                    )
                    movie_exists = cursor.fetchone()

                    if movie_exists is None:
                        cursor.execute(
                            """
                            INSERT INTO user_movie_collection (id_user, id_movie,date)
                            VALUES (%s, %s)
                            """,
                            (id_user, id_movie,date),
                        )
                        connection.commit()
                        print("Insertion successful : movie added.")
                    else:
                        print(f"movie with id {id_movie} already exists in {id_user} collection.")
        except Exception as e:
            print("Insertion error : ", str(e))


    def get_all_collection(self,id_user: int, limit: int = 10, offset: int = 0) -> list:
        try:
            query = f"SELECT * FROM user_movie_collection WHERE id_user = %s LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        return results

    def delete(self, id_user: int, id_movie:int):
        try:
            query = "DELETE FROM user_movie_collection WHERE id_user = %s and id_movie = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_user,id_movie,),
                    )
                    connection.commit()
                    print("Record deleted successfully FROM user_movie_collection.")
        except Exception as e:
            print(f"Error while deleting FROM user_movie_collection: {e}")
            self.db_connection.connection.rollback()
            return None

