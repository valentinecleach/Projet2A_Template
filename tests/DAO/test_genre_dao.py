import pytest
from psycopg2 import OperationalError, connect

from src.DAO.db_connection import DBConnection
from src.DAO.genre_dao import GenreDao
from src.Model.genre import Genre


# Configuration pour la base de données de test
@pytest.fixture(scope="module")
def db_connection():
    try:
        connection = connect(
            dbname="test_db",
            user="username",
            password="password",
            host="localhost",
            port="5432"
        )
        yield connection
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")

@pytest.fixture(scope="module")
def genre_dao(db_connection):
    return GenreDao()

def test_insert_genre(genre_dao):
    # Créer un nouvel objet Genre
    new_genre = Genre(id=28, name="Test Genre")

    # Appel de la méthode insert
    genre_dao.insert(new_genre)

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









