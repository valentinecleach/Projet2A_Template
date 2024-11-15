import pytest
from psycopg2 import OperationalError, connect

from src.DAO.db_connection import DBConnector

from src.DAO.genre_dao import \
    GenreDao  # Assure-toi que cette importation est correcte
from src.Model.genre import \
    Genre  # Assure-toi que l'importation du modèle Genre est correcte

from tests.DAO.test_db import mock_db_connection

# Informations de connexion à la base de données
DB_NAME = "id2464"
DB_USER = "id2464"
DB_PASSWORD = "id2464"
DB_HOST = "sgbd-eleves.domensai.ecole"
DB_PORT = "5432"
DB_SCHEMA = "projet_info_test"  # Utilisation du schéma de test

# Configuration pour la base de données de test
@pytest.fixture(scope="module")
def db_connection():
    try:
        # Connexion à la base de données avec les paramètres donnés
        connection = connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        # Changement de schéma (optionnel si nécessaire)
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO {DB_SCHEMA};')
        yield connection
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")

@pytest.fixture
def genre_dao(mock_db_connection):
    """fixture de GenreDao avec mock_db_connection"""
    mock_connection, mock_cursor = mock_db_connection
    genre_dao_instance = GenreDao(db_connection = mock_connection)
    return genre_dao_instance


def test_insert_new_genre(genre_dao, mock_db_connection):
    """Test insert a genre
    """
    # GIVEN
    # Créer un nouvel objet Genre
    test_genre = Genre(id=28, name="Test Genre")  # Assure-toi que la classe Genre est bien définie dans ton code
    

    # WHEN
    # Appel de la méthode insert
    genre_dao.insert(new_genre)

    # THEN
    # Vérifier que le genre a bien été inséré
    with genre_dao.db_connection.connection.cursor() as cursor:
        cursor.execute("SELECT name_genre FROM Genre WHERE id_genre = %s", (28,))
        result = cursor.fetchone()

    # Assert pour vérifier que le genre inséré est correct
    assert result is not None, "Genre should have been inserted"
    assert result[0] == "Test Genre", "Genre name should match"

    # Nettoyage : supprimer le genre inséré
    with genre_dao.db_connection.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Genre WHERE id_genre = %s", (28,))
            connection.commit()



def test_insert_existing_genre(genre_dao, mock_db_connection):
    """Test insert a genre
    """
    # GIVEN
    # Créer un nouvel objet Genre
    test_genre = Genre(id=28, name="Test Genre")  # Assure-toi que la classe Genre est bien définie dans ton code
    

    # WHEN
    # Appel de la méthode insert
    genre_dao.insert(new_genre)

    # THEN
    # Vérifier que le genre a bien été inséré
    with genre_dao.db_connection.connection.cursor() as cursor:
        cursor.execute("SELECT name_genre FROM Genre WHERE id_genre = %s", (28,))
        result = cursor.fetchone()

    # Assert pour vérifier que le genre inséré est correct
    assert result is not None, "Genre should have been inserted"
    assert result[0] == "Test Genre", "Genre name should match"

    # Nettoyage : supprimer le genre inséré
    with genre_dao.db_connection.connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Genre WHERE id_genre = %s", (28,))
            connection.commit()









