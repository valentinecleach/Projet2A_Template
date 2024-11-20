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
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)
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
                print(f"Rating relationship between {rating.user.username} and {rating.movie.title} already exist. Try an update")
        except Exception as e:
            print("Insertion error:", str(e))

    def update(self, rating: Rating):
        try:
            update_query = """
                UPDATE rating
                SET rating = %s, date = %s
                WHERE id_user = %s AND id_movie = %s;
            """
            values = (rating.rate, rating.date, rating.user.id_user, rating.movie.id_movie)
            self.db_connection.sql_query(update_query, values)
            print(f"Update successful: Rating for {rating.user.username} and {rating.movie.title} updated.")
        except Exception as e:
            print("Update error:", str(e))


    def get_rating(self, id_user: int, id_movie: int) -> Rating:
        try:
            query = "SELECT * FROM rating WHERE id_user = %s AND id_movie = %s"
            result = self.db_connection.sql_query(query, (id_user, id_movie), return_type="one")
            if result:
                user = self.user_dao.get_user_by_id(id_user)
                movie = self.movie_dao.get_by_id(id_movie)

                # Vérification de la validité des objets récupérés
                if user and movie:
                    # Création de l'objet Rating
                    rating = Rating(
                        user=user,
                        movie=movie,
                        date=result["date"],
                        rate=result["rating"]
                    )
                    return rating
                else:
                    print(f" Error while fetching user or Movie (id_user={id_user}, id_movie={id_movie}).")
                    return None
            else:
                print(f"No existing rating beetween {id_user} and Movie {id_movie}.")
                return None
                
        except Exception as e:
            print(f"Error during fetching : {str(e)}")
            return None

    def delete(self, rating: Rating):
        try:
            # Requête DELETE pour supprimer un enregistrement basé sur id_user et id_movie
            query = "DELETE FROM rating WHERE id_user = %s AND id_movie = %s"
            values = (rating.user.id_user, rating.movie.id_movie)
            self.db_connection.sql_query(
                query,
                values)
            print(f"Record deleted successfully from ratings for user {rating.user.id_user} and movie {rating.movie.id_movie}.")
        except Exception as e:
            # Gestion des erreurs et affichage du message d'erreur
            print(f"Error while deleting from ratings: {e}")
            return None


# db_connection = DBConnector()
# my_object= RatingDao(db_connection)
# print(my_object.get_rating(417, 19995))