from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.DAO.user_favorites_dao import UserFavoriteDao
from src.DAO.user_follow_dao import UserFollowDao
from src.Service.movie_service import MovieService


class UserInteractionService:
    """An object that allows interaction between users.

    Attributes
    ----------
    db_connection: DBConnector
        A connector to a database
    user_dao: UserDao
        An object to interact with the database user
    user_follow_dao: UserFollowDao
    user_favourites_dao: UserFavouriteDao
    comment_dao: CommentDao
    movieservice: MovieService

    """

    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.user_follow_dao = UserFollowDao(db_connection)
        self.user_favorites_dao = UserFavoriteDao(db_connection)
        self.comment_dao = CommentDao(db_connection)
        self.movie_service = MovieService(db_connection)

    # def search_user(self, username: str):
    #     """Permet de chercher le profil d'un autre utilisateur."""
    #     if not username:
    #         print("Le nom d'utilisateur est requis.")
    #         return None

    #     users = self.user_dao.get_user_by_name(username)

    #     if users:
    #         return users

    #     print("Aucun utilisateur trouvé pour le nom :", username)
    #     return None

    # # focntionne si correspondance exacte avec le pseudo

    def follow_user(self, follower_id: int, followee_id: int):
        """
        Allows a user to follow another user.

        Parameters
        ----------
        follower_id : int
            The ID of the user who wants to follow.
        followee_id : int
            The ID of the user to be followed.
        """
        # Verifying if the user tries to follow themselves.
        if follower_id == followee_id:
            raise ValueError("A user cannot follow themselves.")
        if (self.user_dao.get_user_by_id(follower_id)) is None:
            raise ValueError(f"This User doesn't exist. Provide a good id")
        try:
            self.user_follow_dao.insert(follower_id, followee_id)
        except Exception as error:
            raise ValueError(f"An error occurred while trying to follow: {error}")

    def unfollow_user(self, follower_id: int, followee_id: int):
        """
        Allows a user to unfollow another user.

        Parameters
        ----------
        follower_id : int
            The ID of the user who wants to unfollow.
        followee_id : int
            The ID of the user to be unfollowed.
        """
        # Verifying if the link between the two users already exists
        if not self.user_follow_dao.is_following(follower_id, followee_id):
            raise ValueError("This user is not being followed.")

        # Deletes the following relationship in the database.
        try:
            self.user_follow_dao.delete(follower_id, followee_id)
        except Exception as error:
            raise ValueError(f"An error occurred while unfollowing: {error}")

    def add_favorite(self, id_user: int, id_movie: int) -> None:
        """
        Allows a user to add a movie to their favorites.

        Parameters
        ----------
        user_id : int
            The ID of the user adding the favorite.
        movie_id : int
            The ID of the movie to be added to favorites.
        """
        # Adds movies to the users favorites if it isn't already done
        try:
            self.user_favorites_dao.insert(id_user, id_movie)
        except Exception as error:
            raise ValueError(f"An error occurred while adding favorite: {error}")

    def delete_favorite(self, user_id: int, id_movie: int) -> None:
        """
        Removes a movie from the user's favorites.

        Parameters
        ----------
        user_id : int
            The ID of the user.
        movie_id : int
            The ID of the movie to remove from favorites.
        """
        # Verifies if the film is already in their favorites
        favorites = self.user_favorites_dao.get_favorites(user_id)

        if id_movie not in favorites:
            raise ValueError("This movie is not in the user's favorites.")

        # Deletes the favorite
        try:
            self.user_favorites_dao.remove(user_id, id_movie)
        except Exception as error:
            raise ValueError(
                f"An error occurred while trying to remove the favorite: {error}"
            )

    def get_user_favorites(self, user_id: int) -> list:
        """
        Retrieves a user's list of favorite movies.

        Parameters
        ----------
        user_id : int
            The ID of the user.

        Returns
        -------
        list
            A list of the user's favorite , or an empty list if no movies are found.
        """
        try:
            favorites = self.user_favorites_dao.get_favorites(user_id)
            return favorites if favorites is not None else []  # Protection against None
        except Exception as error:
            raise ValueError(f"An error occurred while retrieving favorites: {error}")

    # def add_comment(self, comment: Comment):
    #     """
    #     provide a comment to a specific movie.

    #     Parameters
    #     ----------
    #     id_user : int
    #         The ID of the user who is rating.
    #     id_movie : int
    #         The ID of the movie to rate.
    #     comment : str

    #     Returns
    #         None
    #     -------
    #     """
    #     try:
    #         self.comment_dao.insert(comment)
    #     except Exception as error:
    #         raise ValueError(f"An error occurred while commenting the movie: {error}")


# doctest follow_user()
# db_connection = DBConnector()
# user_interaction_service = UserInteractionService(db_connection)
# print(user_interaction_service.search_user("johndoe")) # works
# follower_id = 1
# followee_id = 2
# user_service.follow_user(follower_id, followee_id)
# try:
#     user_service.follow_user(follower_id, followee_id)
# except ValueError as e:
#     print(e)

# try:
# user_service.follow_user(follower_id, follower_id)
# except ValueError as e:
# print(e)

# doctest pour unfollow_user()
# db_connection = DBConnector()
# user_service = UserService(db_connection)
# follower_id = 1
# followee_id = 2
# user_service.follow_user(follower_id, followee_id)
# user_service.unfollow_user(follower_id, followee_id)
# try:
#     user_service.unfollow_user(follower_id, followee_id)
# except ValueError as e:
#     print(e)

# try:
#     user_service.unfollow_user(follower_id, follower_id)
# except ValueError as e:
#     print(e)
# db_connection = DBConnector()
# user_service = UserInteractionService(db_connection)

# user_id = 217
# movie_id = 19995
# user_service.add_favorite(user_id, movie_id)


# invalid_movie_id = 999
# try:
#    user_service.remove_favorite(user_id, invalid_movie_id)
# except ValueError as e:
#    print(e)
