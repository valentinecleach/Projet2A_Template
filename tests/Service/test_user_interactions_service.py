from datetime import datetime
import pytest

from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment

from tests.DAO.follow_dao_test import MockDBConnectorFollowDAO
from tests.DAO.favorite_dao_test import MockDBConnectorFavoriteDAO
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

def test_follow_user_success():
    """Test de la méthode follow_user pour vérifier l'ajout d'une relation de suivi."""
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    follower_id = 1
    user_test = user_dao.get_user_by_id(1)
    followee_id = 2
    while followee_id in user_test.follow_list:
        followee_id += 1
    user_interaction_service.follow_user(follower_id, followee_id)
    query = "SELECT 1 FROM follower WHERE id_user = %s AND id_user_followed = %s;"
    result = db_connection.sql_query(query, (follower_id, followee_id), return_type="one")
    db_connection.sql_query("DELETE FROM follower WHERE id_user = %s AND id_user_followed = %s;", (follower_id, followee_id))
    assert result is not None, "Follow relationship was not created successfully."
    

def test_follow_user_self():
    """Test du cas où un utilisateur essaie de se suivre lui-même."""

    db_connection = DBConnector() 
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    follower_id = 1
    followee_id = 1
    try:
        user_interaction_service.follow_user(follower_id, followee_id)
    except ValueError as e:
        assert str(e) == "A user cannot follow themselves."
    else:
        assert False, "ValueError was not raised."

def test_unfollow_user_not_following():
    """Test du cas où un utilisateur essaie de se désabonner d'un utilisateur qu'il ne suit pas."""

    db_connection = DBConnector()  # Connexion à la base de données
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    follower_id = 1
    user_test = user_dao.get_user_by_id(1)
    followee_id = 2
    while followee_id in user_test.follow_list:
        followee_id += 1
    try:
        user_interaction_service.unfollow_user(follower_id, followee_id)
    except ValueError as e:
        assert str(e) == "This user is not being followed."
    else:
        assert False, "ValueError was not raised."

def test_unfollow_user_success():
    """Test de la méthode unfollow_user pour vérifier la suppression d'une relation de suivi."""

    db_connection = DBConnector() 
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    follower_id = 1
    user_test = user_dao.get_user_by_id(1)
    followee_id = 2
    while followee_id in user_test.follow_list:
        followee_id += 1
    user_interaction_service.follow_user(follower_id, followee_id)
    user_interaction_service.unfollow_user(follower_id, followee_id)
    query = "SELECT 1 FROM follower WHERE id_user = %s AND id_user_followed = %s;"
    result = db_connection.sql_query(query, (follower_id, followee_id), return_type="one")
    db_connection.sql_query(
        "DELETE FROM follower WHERE id_user = %s AND id_user_followed = %s;", (follower_id, followee_id)
    )
    assert result is None, "Follow relationship was not deleted successfully."
    
def test_add_favorite_success():
    """Test de la méthode add_favorite pour vérifier l'ajout d'un film aux favoris."""

    db_connection = DBConnector() 
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    id_user = 1
    user_test = user_dao.get_user_by_id(1)
    id_movie = 102 # we choose a film not in favorite
    user_interaction_service.add_favorite(id_user, id_movie)
    query = "SELECT 1 FROM user_movie_collection WHERE id_user = %s AND id_movie = %s;"
    result = db_connection.sql_query(query, (id_user, id_movie), return_type="one")
    db_connection.sql_query(
        "DELETE FROM user_movie_collection WHERE id_user = %s AND id_movie = %s;", (id_user, id_movie)
    )
    assert result is not None, "Movie was not added to favorites successfully."

def test_delete_favorite_success():
    """Test de la méthode delete_favorite pour vérifier la suppression d'un film des favoris."""

    db_connection = DBConnector() 
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)

    id_user = 1
    user_test = user_dao.get_user_by_id(1)
    own_film_collection = user_test.own_film_collection
    id_movie = own_film_collection[0]
    user_interaction_service.delete_favorite(id_user, id_movie)
    query = "SELECT 1 FROM user_movie_collection WHERE id_user = %s AND id_movie = %s;"
    result = db_connection.sql_query(query, (id_user, id_movie), return_type="one")
    user_interaction_service.add_favorite(id_user, id_movie)
    assert result is None, "Movie was not removed from favorites successfully."

def test_delete_favorite_movie_not_in_favorites():
    """Test de la méthode delete_favorite pour vérifier la levée d'une exception quand le film n'est pas dans les favoris."""

    db_connection = DBConnector()  # Connexion à la base de données
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)

    id_user = 1  # ID de l'utilisateur
    user_test = user_dao.get_user_by_id(1)
    own_film_collection = user_test.own_film_collection
    id_movie = 118 # a movie not in collection
    query = "SELECT 1 FROM user_movie_collection WHERE id_user = %s AND id_movie = %s;"
    result = db_connection.sql_query(query, (id_user, id_movie), return_type="one")
    assert result is None, "This movie should not be in the user's favorites initially."
    with pytest.raises(ValueError, match="This movie is not in the user's favorites."):
        user_interaction_service.delete_favorite(id_user, id_movie)

def test_get_user_favorites_with_favorites():
    """
    Test the get_user_favorites method when a user has favorites.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    user_id = 1
    user_test = user_dao.get_user_by_id(user_id)
    own_film_collection = user_test.own_film_collection
    assert len(own_film_collection) > 0, "The user should have at least one favorite for this test."
    favorites = user_interaction_service.get_user_favorites(user_id)
    assert favorites == own_film_collection, "The favorites returned do not match the database records."


def test_get_user_favorites_without_favorites():
    """
    Test the get_user_favorites method when a user has no favorites.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)
    user_dao = UserDao(db_connection)
    user_id = 1
    user_test = user_dao.get_user_by_id(user_id)
    own_film_collection = user_test.own_film_collection
    for id_movie in own_film_collection:
        user_interaction_service.delete_favorite(user_id, id_movie)
    query = "SELECT COUNT(*) FROM user_movie_collection WHERE id_user = %s;"
    result = db_connection.sql_query(query, (user_id,), return_type="one")
    favorites = user_interaction_service.get_user_favorites(user_id)
    for id_movie in own_film_collection:
        user_interaction_service.add_favorite(user_id, id_movie)
    assert result["count"] == 0, "The user should have no favorites for this test."
    assert favorites == [], "The method should return an empty list when the user has no favorites."


