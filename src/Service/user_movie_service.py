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
    """An object that allows interaction between users and movies.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    user_dao : UserDao
        An object to interact with the database user
    movie_dao : MovieDAO
        An object to interact with movies in the database
    movie_service : MovieService
        An object to interact with movies
    rating_dao : RatingDao
        An object to interact with ratings in the database
    comment_dao : CommentDao
        An object to interact with comments in the database
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)
        self.movie_service = MovieService(db_connection)
        self.rating_dao = RatingDao(db_connection)
        self.comment_dao = CommentDao(db_connection)

    ### For Rating ############

    def get_overall_rating(self, id_movie: int):
        """
        Gets the average rating of the movie.

        Parameters
        ----------
        id_movie : int
            The ID of the movie whose rating we wish to know.

        Returns
        -------
        float | None
            The mean of the rating of the movie. If the rating cannot be calculated, ithe method returns None.
        """
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
        """
        Gets the ratings of a user.

        Parameters
        ----------
        id_user : int
            The ID of a user.
        
        Returns
        -------
        List[Rating]
            A list of all the ratings a user has published. 
            If the user has published no ratings, the method will return None.
        """
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

    def get_ratings_of_follower_for_a_movie(
        self, id_user: int, id_movie: int | None = None
    ):
        """
        If id_movie is specified, the function returns the average rating given by followers for this film.
        Otherwise, the function returns all ratings given by followers.
        
        Parameters
        ----------
        id_user : int
            The ID of the user whose followers we want to observe.
        id_movie : int, optional
            The ID of the movie that we want the average rating if this is what we want.

        Returns
        -------
        list | None
            Either a list of the average rating and the ratings or just a list of ratings depending on the parameters chosen
            If no ratings are found, the method wil return None.
        """
        connected_user = self.user_dao.get_user_by_id(id_user)
        follow_list = connected_user.follow_list
        if follow_list:
            if id_movie:
                ratings = []
                count = 0
                sum_rating = 0
                try:
                    for follow_id in follow_list:
                        rating = self.rating_dao.get_rating(follow_id, id_movie)
                        if rating:
                            ratings.append(rating)
                            count += 1
                            sum_rating += rating.rate
                except Exception as e:
                    print(
                        f"Error while getting follower ratings for a specific movie {id_movie} for user : {id_user}: {e}"
                    )
                if count != 0:
                    return [sum_rating / count, ratings]
                else:
                    print(f"Any follower of user {id_user} rated moovie {id_movie}")
                    return None
            else:
                ratings = []
                try:
                    for follow_id in follow_list:
                        ratings_user = self.get_ratings_user(follow_id)
                        if ratings_user:
                            for rating_user in ratings_user:
                                ratings.append(rating_user)
                except Exception as e:
                    print(
                        f"Error while getting all follower ratings of user: {id_user}: {e}"
                    )
                if ratings != []:
                    return ratings
                else:
                    return None
        else:
            return None

    def delete_user_and_update_ratings(self, id_user: int):
        """
        Allows to delete a user and update all the ratings of the movies he rated.
        
        Parameters
        ----------
        id_user : int
            The ID of the user whose ratings we want to modifie.
        """
        try:
            ratings = self.get_ratings_user(id_user)
            if ratings:
                for rating in ratings:
                    self.delete_a_user_rating(rating)
            self.user_dao.delete_user(id_user)
        except Exception as e:
            print(f"Error while deleting user {id_user}: {e}")

    def delete_a_user_rating(self, rating: Rating):
        """
        Allows to delete a rating.
        
        Parameters
        ----------
        rating : Rating
            The rating to delete
        """
        try:
            movie = rating.movie
            self.rating_dao.delete(rating)
            self.updating_rating_of_movie(movie)
        except Exception as error:
            raise ValueError(
                f"An error occurred while deleting rating for the movie: {error}"
            )

    def count_rating(self, id_movie: int):
        """
        Allows to count the ratings of a movie.
        
        Parameters
        ----------
        id_movie : int
            The ID of a movie.
        """
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
        """
        Allows to update the ratings of a movie.
        
        Parameters
        ----------
        movie : Movie
            A movie.
        """
        movie.vote_average = self.get_overall_rating(movie.id_movie)
        movie.vote_count = self.count_rating(movie.id_movie)
        self.movie_service.movie_dao.update(movie)

    def rate_film_or_update(self, id_user: int, id_movie: int, rate: int):
        """
        Rates a specific movie by providing a score between 0 and 10.

        Parameters
        ----------
        id_user : int
            The ID of the user who is rating.
        id_movie : int
            The ID of the movie to rate.
        rate : int
            The score of the movie on a scale from 0 to 10.
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
        Provides a comment to a specific movie.

        Parameters
        ----------
        id_user : int
            The ID of the user who is rating.
        id_movie : int
            The ID of the movie to rate.
        comment : str
            The new comment to add.
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

    def get_comments_user(self, id_user: int) -> List[Comment]:
        """
        Gets the comments of a user.

        Parameters
        ----------
        id_user : int
            The ID of a user.
        
        Returns
        -------
        List[Comment]
            A list of all the comments a user has published. 
            If the user has published no comments, the method will return None.
        """
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
        """
        Allows to delete a comment.
        
        Parameters
        ----------
        comment : Comment
            The comment to delete
        """
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
# #service.delete_user_and_update_ratings(221)
# # print(type(service.get_ratings_user(305)[0])) # on obtient bien une liste d'objet Rating

# #rating = service.get_ratings_user(305)[0]
# # service.delete_a_user_rating(rating)

# # service.add_or_update_comment(418, 19995, "J'aime les fonds marins de avatar")
# # print(service.get_comments_user(418))
# # service.delete_a_user_comment(service.get_comments_user(418)[0])
