from datetime import datetime

from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment

from tests.DAO.follow_dao_test import MockDBConnectorFollowDAO
from src.Service.user_interactions_service import UserInteractionService

# def test_search_user_found():
#     """
#     Test de la recherche d'un utilisateur.
#     Cette fonction cherche un utilisateur qui existe et vérifie
#     si l'utilisateur est bien retrouvé.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)
#     result = user_interaction_service.search_user("zmason")
#     print(result)
#     assert result is not None  # Vérifie que l'utilisateur est trouvé


# def test_search_user_not_found():
#     """
#     Test de la recherche d'un utilisateur qui n'existe pas.
#     Cette fonction cherche un utilisateur qui n'existe pas
#     et vérifie si la recherche échoue.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)

#     result = user_interaction_service.search_user("unknownuser")
#     print(result)  # Affiche le résultat, qui devrait être None
#     assert result is None  # Vérifie que l'utilisateur n'est pas trouvé


def test_follow_user():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_interaction_service = UserInteractionService(mock_db_connection)
    follower_id = 1
    followee_id = 2
    try:
        user_interaction_service.follow_user(follower_id, follower_id)
    except ValueError as e:
        assert str(e) == "A user cannot follow themselves.", f"Unexpected error message: {e}"
    user_interaction_service.follow_user(follower_id, followee_id)
    assert (follower_id, followee_id) in mock_db_connection.data, "The follow relationship should be added"
    assert mock_db_connection.data[(follower_id, followee_id)] == datetime.now().date(), "Follow date should match"


def test_unfollow_user():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_interaction_service = UserInteractionService(mock_db_connection)
    follower_id = 1
    followee_id = 2
    try:
        user_interaction_service.unfollow_user(follower_id, 999) 
    except ValueError as e:
        assert str(e) == "This user is not being followed.", f"Unexpected error message: {e}"
    mock_db_connection.data[(follower_id, followee_id)] = datetime.now().date() 
    result = user_interaction_service.unfollow_user(follower_id, followee_id)
    assert result is None, "The follow relationship should be removed"


# def test_add_favorite_success():
#     """
#     Test de l'ajout d'un film à la liste des favoris avec succès.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)

#     user_id = 217
#     movie_id = 19965
#     user_interaction_service.add_favorite(user_id, movie_id)
#     print(f"Movie {movie_id} added to User {user_id}'s favorites.")

#     # Vérification si les favoris ont bien été récupérés
#     favorites = user_interaction_service.get_user_favorites(user_id)
#     assert favorites is not None, "Les favoris n'ont pas pu être récupérés."

#     # Vérifier que le film est bien dans les favoris
#     assert movie_id in favorites, "Le film n'a pas été ajouté aux favoris."


# def test_add_favorite_duplicate():
#     """
#     Test où un utilisateur essaie d'ajouter un film déjà présent dans ses favoris.
#     Cela devrait lever une exception.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)

#     user_id = 1
#     movie_id = 100
#     user_interaction_service.add_favorite(user_id, movie_id)  # Premier ajout réussi
#     try:
#         user_interaction_service.add_favorite(user_id, movie_id)  # Deuxième ajout
#     except ValueError as e:
#         print(e)  # Attendu: "This movie is already in favorites."
#         assert str(e) == "This movie is already in favorites."


# def test_get_user_favorites():
#     """
#     Teste la récupération des favoris d'un utilisateur.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)

#     # ID de l'utilisateur
#     user_id = 217

#     # Ajouter deux films aux favoris
#     user_interaction_service.add_favorite(user_id, 19965)
#     user_interaction_service.add_favorite(user_id, 19995)

#     # Récupérer les favoris
#     favorites = user_interaction_service.get_user_favorites(user_id)
#     print(f"Favorites for user {user_id}: {favorites}")

#     # Vérifie que la liste contient les films ajoutés
#     assert 19965 in favorites, "Le film 19965 n'est pas dans les favoris."
#     assert 19995 in favorites, "Le film 19995 n'est pas dans les favoris."


# def test_add_comment():
#     """
#     Teste l'ajout d'un commentaire à un film par un utilisateur.
#     """
#     db_connection = DBConnector()
#     user_interaction_service = UserInteractionService(db_connection)

#     # ID de l'utilisateur et du film
#     user_id = 217
#     movie_id = 19965
#     comment_text = "Super film, vraiment captivant !"

#     # Créer un objet Comment à partir des paramètres
#     user = UserDao(db_connection).get_user_by_id(
#         user_id
#     )  # Récupère l'utilisateur par ID
#     movie = MovieDAO(db_connection).get_by_id(movie_id)  # Récupère le film par ID
#     comment = Comment(
#         user=user, movie=movie, date=datetime.now().date(), comment=comment_text
#     )

#     # Utilisation de la méthode add_comment qui elle, utilise l'insertion via CommentDao
#     user_interaction_service.add_comment(comment)

#     # Vérifier si le commentaire a bien été ajouté, ici il faudra récupérer le commentaire et vérifier son existence
#     comment_dao = CommentDao(db_connection)
#     retrieved_comment = comment_dao.get_comment(user_id, movie_id)

#     assert (
#         retrieved_comment is not None
#     ), "Le commentaire n'a pas été ajouté correctement."
#     assert (
#         retrieved_comment.comment == comment_text
#     ), f"Le commentaire attendu est '{comment_text}', mais on a '{retrieved_comment.comment}'."
