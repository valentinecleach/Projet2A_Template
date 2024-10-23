import pytest

from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnection
from src.Model.comment import Comment


@pytest.fixture(scope="module")
def setup_db():
    """Set up the database connection for testing."""
    # Assurez-vous d'avoir une méthode pour établir une connexion à la base de données pour vos tests.
    db_connection = DBConnection()
    yield db_connection
    db_connection.close()


@pytest.fixture
def insert_test_data(setup_db):
    """Insert test data for a user and movie."""
    connection = DBConnection().connection
    cursor = connection.cursor()

    # Insérer un utilisateur de test
    cursor.execute(
        "INSERT INTO users (username) VALUES (%s) RETURNING id_user", ("test_user",)
    )
    id_user = cursor.fetchone()[0]

    # Insérer un film de test
    cursor.execute(
        "INSERT INTO movie (title) VALUES (%s) RETURNING id_movie", ("Test Movie",)
    )
    id_movie = cursor.fetchone()[0]

    connection.commit()

    return id_user, id_movie


def test_insert_comment(insert_test_data):
    """Test inserting a comment into the database."""
    id_user, id_movie = insert_test_data

    # Créer une instance de CommentDao
    dao = CommentDao()

    # Insérer un commentaire
    comment_text = "Great movie!"
    comment = dao.insert(id_user, id_movie, comment_text)

    # Vérifier que le commentaire inséré n'est pas None et contient les bonnes données
    assert comment is not None
    assert comment.comment == comment_text
    assert comment.user.id_user == id_user
    assert comment.movie.id_movie == id_movie

    # Optionnel : Nettoyer après le test
    dao.delete(
        comment
    )  # Supposons que vous ayez une méthode pour supprimer le commentaire inséré
