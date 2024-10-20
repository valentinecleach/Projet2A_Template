from datetime import datetime
from typing import List  # , Optional

from DAO.db_connection import DBConnection, Singleton
from DAO.movie_dao import MovieDao
from DAO.user_dao import UserDao
from Model.comment import Comment
from Model.movie import Movie


class CommentDao(metaclass=Singleton):
    # CREATE
    def insert(self, id_user: int, id_movie: int, comments: str):
        date = datetime.now()
        if comments:
            values = (id_user, id_movie, comments, date)
            res = DBConnection().insert(cine.comment, values)
        else:
            return None
        if res:
            user = UserDao().get_user_by_id(id_user)
            movie = MovieDao().get_user_by_id(id_movie)
            return Comment(user=user, movie=movie, date=date, comment=comments)

    # READ (Fetch a specific user's comment)
    def get_user(
        self,
        id_user: int,
        id_movie: int,
    ) -> List[Comment]:

        try:
            query = "SELECT * FROM cine.comment WHERE id_user = %s and id_movie = %s"
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
