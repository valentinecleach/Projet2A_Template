from datetime import datetime

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.singleton import Singleton
from src.DAO.user_dao import UserDao
from src.Model.rating import Rating

# from typing import List  # , Optional


class RatingDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection

    # CREATE
    def insert(self, rating: Rating):
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM rating
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (rating.user.id_user, rating.movie.id_movie),
                return_type="one",
            )
            rating_exists = result["count"] > 0 if result else False
            if not rating_exists:
                print("Inserting rating relationship.")
                insert_query = """
                    INSERT INTO rating (id_user, id_movie, rating, date)
                    VALUES (%s, %s, %s, %s);
                """
                values = (
                    rating.user.id_user,
                    rating.movie.id_movie,
                    rating.rate,
                    rating.date,
                )
                self.db_connection.sql_query(insert_query, values)
                print(
                    f"Insertion successful: Rating relationship between {rating.user.username} and {rating.movie.title} added."
                )
            else:
                print(
                    f"Rating relationship between {rating.user.username} and {rating.movie.title} already exist."
                )
        except Exception as e:
            print("Insertion error:", str(e))

    # READ (Fetch all follower) #####################changer en utilisant objet Rating.
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
    def delete(self, rating: Rating):
        id_user = rating.user
        id_movie = rating.movie
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
