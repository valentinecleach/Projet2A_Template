from datetime import datetime
from src.Model.rating import Rating
from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.Service.movie_service import MovieService
from src.DAO.rating_dao import RatingDao
from src.DAO.user_dao import UserDao


class UserMovieService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.movie_service = MovieService(db_connection)
        self.rating_dao = RatingDao(db_connection)
        self.comment_dao = CommentDao(db_connection)

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

    def rate_film_or_update(self, id_user: int, id_movie: int, rate: int):
        """
        Rate a specific movie by providing a score between 0 and 10.

        Parameters
        ----------
        id_user : int
            The ID of the user who is rating.
        id_movie : int
            The ID of the movie to rate.
        rating : int
            The score of the movie 0-10.

        Returns
        -------
        """
        if rate > 10 or rate < 0:
            raise ValueError("the rating must be an integer between 0-10")
        try:
            movie = self.movie_service.get_movie_by_id(id_movie)
            date = datetime.now().date()
            connected_user = self.user_dao.get_user_by_id(id_user)
            rating = Rating(user = connected_user, movie = movie, date = date, rate = rate)
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
            if rating_exists:
                print("Updating rating relationship.")
                self.rating_dao.update(rating)
            else:
                print(f"Rating relationship between {rating.user.username} and {rating.movie.title} does not exist, so we add it.")
                self.rating_dao.insert(rating)
            # changer la moyenne du film et le nombre de votant (Clément s'en occupe)
            # mean = get_overall_rating(id_movie)
            # count = count_rating(id_movie)
            # self.movie_dao.update(movie)

        except Exception as error:
            raise ValueError(f"An error occurred while rating the movie: {error}")


    def add_comment(self, id_user: int, id_movie: int, comment: str):
        """
        provide a comment to a specific movie.

        Parameters
        ----------
        id_user : int
            The ID of the user who is rating.
        id_movie : int
            The ID of the movie to rate.
        comment : str

        Returns
            None
        -------
        """
        try:
            self.comment_dao.insert(id_user, id_movie, comment)
        except Exception as error:
            raise ValueError(f"An error occurred while commenting the movie: {error}")


# db_connection = DBConnector()

# # u = CommentDao(db_connection)
# service = UserMovieService(db_connection)
# # service.add_comment(224, 321, "j'adore ce film")
# service.rate_film_or_update(417, 19995, 9)
