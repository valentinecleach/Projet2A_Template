from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.rating_dao import RatingDao
from src.DAO.user_dao import UserDao


class UserMovieService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)
        self.rating_dao = RatingDao(db_connection)
        self.comment_dao = CommentDao(db_connection)

    def rate_movie(self, id_user: int, id_movie: int, rating: int):
        """
        Rate a specific movie by providing a score between 0 and 10.

        Parameters
        -----------
        id_user : int
            The ID of the user who is rating.
        id_movie : int
            The ID of the movie to rate.
        rating : int
            The score of the movie 0-10.

        Returns
        -------
        """
        try:
            float(rating)
        except Exception:
            raise ValueError("Enter a number between 0-10")
        if rating > 10 or rating < 0:
            raise ValueError("the rating must be between 0-10")
        res = self.rating_dao.get_rating(id_user, id_movie)
        if res:
            raise ValueError(
                f"You have already rate this movie {res.rating} over 10 on {res.date}"
            )

        else:
            try:
                self.rating_dao.insert(id_user, id_movie, rating)
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

# u = CommentDao(db_connection)
# service = UserMovieService(db_connection)
# service.add_comment(224, 321, "j'adore ce film")
