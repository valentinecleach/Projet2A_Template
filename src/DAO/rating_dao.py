from datetime import datetime

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.singleton import Singleton
from src.DAO.user_dao import UserDao
from src.Model.rating import Rating


class RatingDao(metaclass=Singleton):
    """RatingDao is DAO for managing ratings of movies by users in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    movie_dao : MovieDao
        A DAO object used for operations related to movies.
    user_dao : MovieDao
        A DAO object used for operations related to users.
    """

    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)

    def insert(self, rating: Rating):
        """Inserts a new rating into the Database.

        Parameters:
        -----------
        rating : Rating
            A rating to add.
        """
        try:
            # Verifying the existence of a link
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
                    f"Rating relationship between {rating.user.username} and {rating.movie.title} already exist. Try an update"
                )
        except Exception as e:
            print("Insertion error:", str(e))

    def update(self, rating: Rating):
        """Updates an existing rating in the Database.

        Parameters:
        -----------
        rating : Rating
            A new rating to overwrite the old one.
        """
        try:
            update_query = """
                UPDATE rating
                SET rating = %s, date = %s
                WHERE id_user = %s AND id_movie = %s;
            """
            values = (
                rating.rate,
                rating.date,
                rating.user.id_user,
                rating.movie.id_movie,
            )
            self.db_connection.sql_query(update_query, values)
            print(
                f"Update successful: Rating for {rating.user.username} and {rating.movie.title} updated."
            )
        except Exception as e:
            print("Update error:", str(e))

    def get_rating(self, id_user: int, id_movie: int) -> Rating:
        """Selects a rating from the database from a specific user and about a specific movie

        Parameters
        ----------
        id_user: int
            The ID of the user whose rating we want to select.
        id_movie : int
            The ID of the movie which the rating is about.

        Returns
        -------
        Rating | None
            The rating of the movie selected.
            If the rating doesn't exist, the method will return None.
        """
        try:
            query = "SELECT * FROM rating WHERE id_user = %s AND id_movie = %s"
            result = self.db_connection.sql_query(
                query, (id_user, id_movie), return_type="one"
            )
            if result:
                user = self.user_dao.get_user_by_id(id_user)
                movie = self.movie_dao.get_by_id(id_movie)

                # Verifying the validity of the objects retrieved
                if user and movie:
                    # Creation of an instance of Rating
                    rating = Rating(
                        user=user,
                        movie=movie,
                        date=result["date"],
                        rate=result["rating"],
                    )
                    return rating
                else:
                    print(
                        f" Error while fetching user or Movie (id_user={id_user}, id_movie={id_movie})."
                    )
                    return None
            else:
                print(f"No existing rating beetween {id_user} and Movie {id_movie}.")
                return None

        except Exception as e:
            print(f"Error during fetching : {str(e)}")
            return None

    def delete(self, rating: Rating):
        """Deletes a rating.

        Parameters
        ----------
        rating : Rating
            A rating to delete
        """
        try:
            # Request to delete a a rating based on the users ID and the movies ID.
            query = "DELETE FROM rating WHERE id_user = %s AND id_movie = %s"
            values = (rating.user.id_user, rating.movie.id_movie)
            self.db_connection.sql_query(query, values)
            print(
                f"Record deleted successfully from ratings for user {rating.user.id_user} and movie {rating.movie.id_movie}."
            )
        except Exception as e:
            # Error handling and displaying the error message.
            print(f"Error while deleting from ratings: {e}")
            return None
