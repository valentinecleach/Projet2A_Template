from datetime import datetime

from src.DAO.db_connection import DBConnection, Singleton
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.rating import Rating

# from typing import List  # , Optional


class RatingDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnection):
        # create a DB connection object
        self.db_connection = db_connection
        # Create tables if don't exist
        self.db_connection.create_tables()

    # CREATE
    def insert(self, id_user: int, id_movie: int, rate: int):
        date = datetime.now()
        if rate >= 0 and rate <= 10:
            values = (id_user, id_movie, rate, date)
            date = datetime.now()
            try:
                with self.db_connection.connection.cursor() as cursor:
                    query = f"INSERT INTO rating(id_user, id_movie, rate, date) VALUES ({', '.join(['%s'] * len(values))})"
                    res = cursor.execute(query, values)
                    self.db_connection.connection.commit()
            except Exception as e:
                print(f"Erreur lors de l'insertion dans rating: {str(e)}")
                self.db_connection.connection.rollback()
                return None
        if res:
            user = UserDao().get_user_by_id(id_user)
            movie = MovieDao().get_by_id(id_movie)
            rate = Rating(user=user, movie=movie, date=date, rating=rate)
            return rate

    # READ (Fetch all follower)
    def get_rating(
        self,
        id_user: int,
        id_movie: int,
    ) -> Rating:

        try:
            query = "SELECT * FROM  rating WHERE id_user = %s and id_movie = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user, id_movie))
                    res = cursor.fetchone()
            if res:
                user = UserDao().get_user_by_id(id_user)
                movie = MovieDao().get_by_id(id_movie)
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
            query = "DELETE FROM  rating WHERE id_user = %s and id_movie = %s"
            with self.db_connection.connection as connection:
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
            self.db_connection.connection.rollback()
            return None

    def get_overall_rating(id_movie: int):
        try:
            query = "SELECT AVG(rate) as mean  FROM  rating WHERE id_movie = %s"
            with self.db_connection.connection as connection:
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

    def count_rating(id_movie: int):
        try:
            query = "SELECT count(*) as number  FROM  rating WHERE id_movie = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_movie,),
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Error while counting ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]
