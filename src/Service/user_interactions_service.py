from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.DAO.user_favorites_dao import UserFavoriteDao
from src.DAO.user_follow_dao import UserFollowDao


class UserInteractionService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)
        self.user_follow_dao = UserFollowDao(db_connection)
        self.user_favorites_dao = UserFavoriteDao(db_connection)

    def search_user(self, username: str):
        """Permet de chercher le profil d'un autre utilisateur."""
        if not username:
            print("Le nom d'utilisateur est requis.")
            return None

        users = self.user_dao.get_user_by_name(username)

        if users:
            return users

        print("Aucun utilisateur trouvé pour le nom :", username)
        return None

    # focntionne si correspondance exacte avec le pseudo

    def follow_user(
        self, follower_id: int, followee_id: int
    ) -> None:  ## follower_id doit être récupéré avec la connection
        """
        Allows a user to follow another user.

        Parameters
        ----------
        follower_id : int
            The ID of the user who wants to follow.
        followee_id : int
            The ID of the user to be followed.
        """
        # Vérifier si l'utilisateur essaie de se suivre lui-même
        if follower_id == followee_id:
            raise ValueError("A user cannot follow themselves.")

        # Ajouter le suivi en base de données si la relation n'existe pas déjà
        try:
            self.user_follow_dao.insert(follower_id, followee_id)
        except Exception as error:
            raise ValueError(f"An error occurred while trying to follow: {error}")

    def unfollow_user(self, follower_id: int, followee_id: int) -> None:
        """
        Allows a user to unfollow another user.

        Parameters
        ----------
        follower_id : int
            The ID of the user who wants to unfollow.
        followee_id : int
            The ID of the user to be unfollowed.
        """
        # Vérifier si l'utilisateur essaie de se désabonner de lui-même
        if follower_id == followee_id:
            raise ValueError("A user cannot unfollow themselves.")

        # Vérifier si le lien de suivi existe (ou utilisez une méthode comme follow_dao.is_following)
        if not self.user_follow_dao.is_following(follower_id, followee_id):
            raise ValueError("This user is not being followed.")

        # Supprimer le suivi en base de données
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
        # Ajouter le film en favori si ce n'est pas déjà fait
        try:
            self.user_favorites_dao.insert(id_user, id_movie)
        except Exception as error:
            raise ValueError(f"An error occurred while adding favorite: {error}")

    def remove_favorite(self, user_id: int, movie_id: int) -> None:
        """
        Removes a movie from the user's favorites.

        Parameters
        ----------
        user_id : int
            The ID of the user.
        movie_id : int
            The ID of the movie to remove from favorites.
        """
        # Vérification si le film est dans les favoris
        favorites = self.user_favorites_dao.get_favorites(user_id)
        favorite_ids = [fav["id_movie"] for fav in favorites]

        if movie_id not in favorite_ids:
            raise ValueError("This movie is not in the user's favorites.")

        # Suppression du favori
        try:
            self.user_favorites_dao.delete(user_id, movie_id)
        except Exception as error:
            raise ValueError(
                f"An error occurred while trying to remove the favorite: {error}"
            )

    def get_user_favorites(self, user_id: int) -> list:
        """
        Retrieves the list of favorite movies for a user.

        Parameters
        ----------
        user_id : int
            The ID of the user whose favorites are to be retrieved.

        Returns
        -------
        list
            A list of favorite movies for the user.
        """
        try:
            return self.user_favorite_dao.get_favorites(user_id)
        except Exception as error:
            raise ValueError(f"An error occurred while retrieving favorites: {error}")

    def rate_film(self, film, rating: int):
        """Attribue une note à un film."""

    def add_comment(self, film, comment: str):
        """Ajoute un commentaire à un film."""

    def log_out(self):
        """Déconnexion de l'utilisateur."""

    def delete_account(self):
        """Suppression du compte de l'utilisateur."""


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

# # doctest pour unfollow_user()
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
db_connection = DBConnector()
user_favorite_dao = UserFavoriteDao(db_connection)
user_service = UserInteractionService(user_favorite_dao)

user_id = 1
movie_id = 42
user_service.add_favorite(user_id, movie_id)

# user_service.remove_favorite(user_id, movie_id)

# try:
#    user_service.remove_favorite(user_id, movie_id)
# except ValueError as e:
#    print(e)

# invalid_movie_id = 999
# try:
#    user_service.remove_favorite(user_id, invalid_movie_id)
# except ValueError as e:
#    print(e)
