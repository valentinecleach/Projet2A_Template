from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnection, Singleton
from src.Model.movie_collection import MovieCollection


class MovieCollectionDao(metaclass=Singleton):
    # CREATE collection
    def insert(id_collection: int, name: str):
        values = (id_collection, name)
        res = DBConnection().insert(cine.movie_collection, values)
        if res:
            return MovieCollection(id=id_collection, name=name)

    # READ (Fetch a specific user's comment)
    def get_movie_collection_by_id(
        self,
        id_collection: int,
    ) -> MovieCollection:

        try:
            query = "SELECT * FROM cine.movie _collection WHERE id_collection = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_collection))
                    res = cursor.fetchone()
            if res:
                return MovieCollection(id=id_collection, name=res["name"])
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
            query = f"SELECT * FROM cine.movie_collection LIMIT {max(limit, 0)}"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                    )
                    results = cursor.fetchall()
            if results:
                coll = [
                    MovieCollection(name=res["name"], id=res["id_collection"])
                    for res in results
                ]
                return coll
            else:
                return None
        except Exception:
            return None

    # DELETE
    def delete(self, id_collection):
        try:
            query = "DELETE FROM cine.movie_collection WHERE id_collection = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_collection),
                    )
                    connection.commit()
                    print("Record deleted successfully from movie collection.")
        except Exception as e:
            print(f"Error while deleting from movie collection: {e}")
            return None
