import pytest
from datetime import datetime
from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.DAO.movie_dao import MovieDAO
from src.Model.comment import Comment
from src.Model.user import User
from src.Model.movie import Movie


@pytest.fixture(scope="module")
def db_connection():
    """Initialise la connexion à la base de données pour les tests."""
    return DBConnector()  # Pas besoin d'appeler close ici


@pytest.fixture(scope="module")
def comment_dao(db_connection):
    """Fixture pour CommentDao."""
    return CommentDao(db_connection)

@pytest.fixture(scope="module")
def user_and_movie(db_connection):
    """Fixture pour récupérer un utilisateur et un film valides."""
    user_dao = UserDao(db_connection)
    movie_dao = MovieDAO(db_connection)

    user = user_dao.get_user_by_id(1)  # Assurez-vous qu'un utilisateur avec cet ID existe
    movie = movie_dao.get_by_id(1)  # Assurez-vous qu'un film avec cet ID existe

    return user, movie

def test_insert_comment(comment_dao, user_and_movie):
    """Test l'insertion d'un commentaire."""
    user, movie = user_and_movie

    if user and movie:
        comment = Comment(user=user, movie=movie, comment="Great movie!", date="2024-11-21")
        comment_id = comment_dao.insert(comment)

        assert comment_id is not None, "L'insertion du commentaire a échoué"

def test_get_comment_by_id(comment_dao, user_and_movie):
    """Test la récupération d'un commentaire par ID."""
    user, movie = user_and_movie

    if user and movie:
        comment = Comment(user=user, movie=movie, comment="Amazing visuals!", date="2024-11-21")
        comment_id = comment_dao.insert(comment)

        fetched_comment = comment_dao.get_by_id(comment_id)
        assert fetched_comment is not None, "Le commentaire n'a pas pu être récupéré."
        assert fetched_comment.comment == "Amazing visuals!", "Le contenu du commentaire ne correspond pas."

def test_delete_comment(comment_dao, user_and_movie):
    """Test la suppression d'un commentaire."""
    user, movie = user_and_movie

    if user and movie:
        comment = Comment(user=user, movie=movie, comment="To be deleted", date="2024-11-21")
        comment_id = comment_dao.insert(comment)

        deleted = comment_dao.delete(comment_id)
        assert deleted, "La suppression du commentaire a échoué."

        # Vérifier que le commentaire n'existe plus
        fetched_comment = comment_dao.get_by_id(comment_id)
        assert fetched_comment is None, "Le commentaire n'a pas été supprimé."

def test_get_comments_for_movie(comment_dao, user_and_movie):
    """Test la récupération des commentaires d'un film."""
    user, movie = user_and_movie

    if user and movie:
        # Ajouter quelques commentaires
        comment1 = Comment(user=user, movie=movie, comment="Loved the story!", date="2024-11-21")
        comment2 = Comment(user=user, movie=movie, comment="Great acting!", date="2024-11-22")

        comment_dao.insert(comment1)
        comment_dao.insert(comment2)

        comments = comment_dao.get_by_movie_id(movie.id)
        assert len(comments) >= 2, "Tous les commentaires pour le film n'ont pas été récupérés."
        assert any(c.comment == "Loved the story!" for c in comments), "Le commentaire 'Loved the story!' est manquant."
        assert any(c.comment == "Great acting!" for c in comments), "Le commentaire 'Great acting!' est manquant."