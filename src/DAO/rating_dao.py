from datetime import datetime

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.singleton import Singleton
from src.DAO.tables_creation import TablesCreation
from src.DAO.user_dao import UserDao
from src.Model.rating import Rating

# from typing import List  # , Optional


class RatingDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection
        # Create tables if don't exist
        self.tables_creation = TablesCreation(db_connection)

    # CREATE
    def insert(self, id_user: int, id_movie: int, rate: int):
        try:
            user = UserDao(self.db_connection).get_user_by_id(id_user)
            movie = MovieDAO(self.db_connection).get_by_id(id_movie)
        except Exception as e:
            print(f"Erreur lors de la recherche du film: {str(e)}")
            return None
        date = datetime.now()
        if rate >= 0 and rate <= 10:
            values = (id_user, id_movie, rate, date)
            date = datetime.now()
            try:
                query = f"INSERT INTO rating(id_user, id_movie, rating, date) VALUES ({', '.join(['%s'] * len(values))})"
                res = self.db_connection.sql_query(query, values)
            except Exception as e:
                print(f"Erreur lors de l'insertion dans rating: {str(e)}")
                return None
        if res:
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
            res = self.db_connection.sql_query(
                query, (id_user, id_movie), return_type="one"
            )
            if res:
                user = UserDao(self.db_connection).get_user_by_id(id_user)
                movie = MovieDAO(self.db_connection).get_by_id(id_movie)
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
            self.db_connection.sql_query(
                query,
                (
                    id_user,
                    id_movie,
                ),
                return_type="one",
            )
            print("Record deleted successfully from ratings.")
        except Exception as e:
            print(f"Error while deleting from ratings: {e}")
            return None

    def get_overall_rating(self, id_movie: int):
        try:
            query = "SELECT AVG(rating) as mean  FROM  rating WHERE id_movie = %s"
            res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
        except Exception as e:
            print(f"Error while averaging ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["mean"]

    def count_rating(self, id_movie: int):
        try:
            query = "SELECT count(*) as number  FROM  rating WHERE id_movie = %s"
            res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
        except Exception as e:
            print(f"Error while counting ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]
