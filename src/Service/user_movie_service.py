from datetime import datetime
from typing import List

from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.rating_dao import RatingDao
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment
from src.Model.movie import Movie
from src.Model.rating import Rating
from src.Service.movie_service import MovieService


class UserMovieService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)
        self.movie_service = MovieService(db_connection)
        self.rating_dao = RatingDao(db_connection)
        self.comment_dao = CommentDao(db_connection)

    ### For Rating ############

    def get_overall_rating(self, id_movie: int):
        try:
            query = "SELECT AVG(rating) as mean  FROM  rating WHERE id_movie = %s"
            res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
        except Exception as e:
            print(f"Error while averaging ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["mean"]
        else:
            return None

    def get_ratings_user(self, id_user: int) -> List[Rating]:
        try:
            connected_user = self.user_dao.get_user_by_id(id_user)
            query = "SELECT id_movie, date, rating FROM rating where id_user = %s"
            res = self.db_connection.sql_query(query, (id_user,), return_type="all")
            ratings = []
            for result in res:
                rate = dict(result)
                movie = self.movie_service.get_movie_by_id(rate["id_movie"])
                rating = Rating(
                    user=connected_user,
                    movie=movie,
                    date=result["date"],
                    rate=result["rating"],
                )
                ratings.append(rating)
            if ratings != []:
                return ratings
            else:
                print(
                    f" The user {connected_user} hasn't rate any moovie for the moment."
                )
                return None
        except Exception as e:
            print(f"Error while finding user {id_user} ratings: {e}")

    def delete_user_and_update_ratings(self, id_user: int):
        try:
            ratings = self.get_ratings_user(id_user)
            for rating in ratings:
                self.delete_a_user_rating(rating)
            self.user_dao.delete_user(id_user)
        except Exception as e:
            print(f"Error while deleting user {id_user}: {e}")

    def get_ratings_user_follower(self, id_user, id_movie: Optional[int] = None):
        connected_user = self.user_dao.get_user_by_id(id_user)
        list_follower = connected_user.follow_list
        if id_movie:
            pass
        else:
            pass

    def delete_a_user_rating(self, rating: Rating):
        try:
            movie = rating.movie
            self.rating_dao.delete(rating)
            self.updating_rating_of_movie(movie)
        except Exception as error:
            raise ValueError(
                f"An error occurred while deleting rating for the movie: {error}"
            )

    def count_rating(self, id_movie: int):
        try:
            query = "SELECT count(*) as number  FROM  rating WHERE id_movie = %s"
            res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
        except Exception as e:
            print(f"Error while counting ratings of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]
        else:
            return None

    def updating_rating_of_movie(self, movie: Movie):
        movie.vote_average = self.get_overall_rating(movie.id_movie)
        movie.vote_count = self.count_rating(movie.id_movie)
        self.movie_service.movie_dao.update(movie)

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
            rating = Rating(user=connected_user, movie=movie, date=date, rate=rate)
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
                self.updating_rating_of_movie(movie)
            else:
                print(
                    f"Rating relationship between {rating.user.username} and {rating.movie.title} does not exist, so we add it."
                )
                self.rating_dao.insert(rating)
                self.updating_rating_of_movie(movie)

        except Exception as error:
            raise ValueError(f"An error occurred while rating the movie: {error}")

    #### For comment ####

    def add_or_update_comment(self, id_user: int, id_movie: int, comment: str):
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
            movie = self.movie_service.get_movie_by_id(id_movie)
            date = datetime.now().date()
            connected_user = self.user_dao.get_user_by_id(id_user)
            new_comment = Comment(
                user=connected_user, movie=movie, date=date, comment=comment
            )
            query = """
                SELECT COUNT(*) as count FROM comment
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (new_comment.user.id_user, new_comment.movie.id_movie),
                return_type="one",
            )
            comment_exist = result["count"] > 0 if result else False
            if comment_exist:
                print("Updating comment relationship.")
                self.comment_dao.update(new_comment)
            else:
                print(
                    f"Comment relationship between {new_comment.user.username} and {new_comment.movie.title} does not exist, so we add it."
                )
                self.comment_dao.insert(new_comment)
        except Exception as error:
            raise ValueError(f"An error occurred while commenting the movie: {error}")

    def get_comments_user(self, id_user: int) -> List[Rating]:
        try:
            connected_user = self.user_dao.get_user_by_id(id_user)
            query = "SELECT id_movie, date, comment FROM comment where id_user = %s"
            res = self.db_connection.sql_query(query, (id_user,), return_type="all")
            comments = []
            for result in res:
                comment_res = dict(result)
                movie = self.movie_service.get_movie_by_id(comment_res["id_movie"])
                comment = Comment(
                    user=connected_user,
                    movie=movie,
                    date=comment_res["date"],
                    comment=comment_res["comment"],
                )
                comments.append(comment)
            if comments != []:
                return comments
            else:
                print(
                    f" The user {connected_user} didn't comment any moovie for the moment."
                )
                return None
        except Exception as e:
            print(f"Error while finding user {id_user} comments: {e}")

    def delete_a_user_comment(self, comment: Comment):
        try:
            movie = comment.movie
            self.comment_dao.delete(comment)
        except Exception as error:
            raise ValueError(
                f"An error occurred while deleting comment for the movie: {error}"
            )


# db_connection = DBConnector()

# # u = CommentDao(db_connection)
# service = UserMovieService(db_connection)
# #service.rate_film_or_update(221, 19995, 5)
# service.delete_user_and_update_ratings(221)
# # print(type(service.get_ratings_user(305)[0])) # on obtient bien une liste d'objet Rating

# #rating = service.get_ratings_user(305)[0]
# # service.delete_a_user_rating(rating)

# # service.add_or_update_comment(418, 19995, "J'aime les fonds marins de avatar")
# # print(service.get_comments_user(418))
# # service.delete_a_user_comment(service.get_comments_user(418)[0])
