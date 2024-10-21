from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnection, Singleton
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie
from src.Model.movie_collection import MovieCollection


class MovieCollectionDao(metaclass=Singleton):
    # CREATE collection
    def insert_collection(self, id_user: int, id_collection: int, name: str):
        date = datetime.now()
        values = (id_user, id_collection, name, date)
        res = DBConnection().insert(cine.collection, values)
        if res:
            user = UserDao().get_user_by_id(id_user)
            return MovieCollection(user=user, date=date, name = name)
    
    # insert movie in a specific collection
    def insert_movie(self, id_movie: int, id_collection: int):
        date = datetime.now()
        values = (id_collection, id_movie, date)
        res = DBConnection().insert(cine.movie_collection, values)
        if res:
            user = UserDao().get_user_by_id(id_user)
            collection = self.get_collection_by_id(id_collection)
            collection.
            return MovieCollection(user=user, date=date, name = name)

    # READ (Fetch a specific user's comment)
    def get_collection_by_id(
        self,
        id_collection: int,
    ) -> List[MovieCollection]:

        try:
            query = "SELECT * FROM cine.collection JOIN cine.movie_collection USING(id_collection)
             WHERE id_collection = %s and id_movie = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user, id_movie))
                    results = cursor.fetchall()
            if res:
                user = UserDao().get_user_by_id(id_user)
                movie = MovieDao().get_user_by_id(id_movie)
                com = [
                    Comment(
                        user=user, movie=movie, date=res["date"], comment=res["comment"]
                    )
                    for res in results
                ]
                return com
            else:
                return None
        except Exception:
            return None

    # READ (Fetch all comments of a specific movie)
    def get_recent(
        self,
        id_movie: int,
        limit: int = 10,
    ) -> List[Comment]:

        try:
            query = f"SELECT * FROM cine.comment WHERE id_movie = %s ORDER BY date DESC LIMIT {max(limit, 0)}"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_movie))
                    results = cursor.fetchall()
            if res:
                user = UserDao().get_user_by_id(id_user)
                movie = MovieDao().get_user_by_id(id_movie)
                com = [
                    Comment(
                        user=user, movie=movie, date=res["date"], comment=res["comment"]
                    )
                    for res in results
                ]
                return com
            else:
                return None
        except Exception:
            return None

    # DELETE
    def delete(self, com: Comment):
        id_user = com.id_user
        id_movie = com.id_movie
        date = com.date
        try:
            query = "DELETE FROM cine.comment WHERE id_user = %s and id_movie = %s and date = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_movie,
                            date,
                        ),
                    )
                    connection.commit()
                    print("Record deleted successfully from comments.")
        except Exception as e:
            print(f"Error while deleting from comments: {e}")
            return None

    def get_overall(movie: Movie):
        id_movie = movie.id_movie
        try:
            query = "SELECT COUNT(*) as number FROM cine.comment WHERE id_movie = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_movie,),
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Error while averaging comments of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]
