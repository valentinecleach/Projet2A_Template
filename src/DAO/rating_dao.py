from datetime import datetime

from src.DAO.db_connection import DBConnection, Singleton
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.rating import Rating

# from typing import List  # , Optional


class RatingDao(metaclass=Singleton):
    # CREATE
    def insert(self, id_user: int, id_movie: int, rating: int):
        date = datetime.now()
        if rating >= 0 and rating <= 10:
            values = (id_user, id_movie, rating, date)
            res = DBConnection().insert(cine.rating, values)
        else:
            return None
        if res:
            user = UserDao().get_user_by_id(id_user)
            movie = MovieDao().get_user_by_id(id_movie)
            rate = Rating(user=user, movie=movie, date=date, rating=rating)
            return rate

    # READ (Fetch all follower)
    def get_rating(
        self,
        id_user: int,
        id_movie: int,
    ) -> Rating:

        try:
            query = "SELECT * FROM cine.rating WHERE id_user = %s and id_movie = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user, id_movie))
                    res = cursor.fetchone()
            if res:
                user = UserDao().get_user_by_id(id_user)
                movie = MovieDao().get_user_by_id(id_movie)
                rate = Rating(
                    user=user, movie=movie, date=res["date"], rating=res["rating"]
                )
                return rate
            else:
                return None
        except Exception:
            return None

    # DELETE
    def delete(self, id_user: int, id_movie: int):
        try:
            query = "DELETE FROM cine.rating WHERE id_user = %s and id_movie = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_movie,
                        ),
                    )
                    connection.commit()
                    print("Record deleted successfully from ratings.")
        except Exception as e:
            print(f"Error while deleting from ratings: {e}")
            return None

    def get_overall_rating(id_movie: int):
        try:
            query = "SELECT AVG(rating) as mean  FROM cine.rating WHERE id_movie = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_movie,),
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Error while averaging ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["mean"]
