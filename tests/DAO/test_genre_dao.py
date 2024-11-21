import pytest
from psycopg2 import connect, OperationalError

from src.DAO.genre_dao import GenreDao
from src.Model.genre import Genre

# Informations de connexion à la base de données
DB_NAME = "id2464"
DB_USER = "id2464"
DB_PASSWORD = "id2464"
DB_HOST = "sgbd-eleves.domensai.ecole"
DB_PORT = "5432"
DB_SCHEMA = "projet_info_test"

# Configuration de la base de données pour le test
@pytest.fixture(scope="module")
def db_connection():
    """Fixture de connexion à la base de données pour le module"""
    try:
        connection = connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO {DB_SCHEMA};')
        yield connection
        connection.close()
    except OperationalError as e:
        pytest.fail(f"Unable to connect to the database: {e}")


@pytest.fixture
def genre_dao(db_connection):
    """Fixture de GenreDao avec une connexion à la base de données"""
    return GenreDao(db_connection=db_connection)

# Test de l'insertion d'un genre
def test_insert_new_genre(genre_dao, db_connection):
    """Test l'insertion d'un genre"""
    test_genre = Genre(id=28, name="Test Genre")

    # WHEN: Appel de la méthode insert pour ajouter un genre
    genre_dao.insert(test_genre)

    # THEN: Vérification que le genre a bien été inséré dans la base de données
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT name_genre FROM genre WHERE id_genre = %s;", (28,))
        result = cursor.fetchone()

    # Vérification de l'insertion
    assert result is not None, "Genre should have been inserted"
    assert result[0] == "Test Genre", "Genre name should match"

    # Nettoyage : supprimer le genre inséré
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM genre WHERE id_genre = %s;", (28,))
        db_connection.commit()

# Test de l'insertion d'un genre déjà existant
def test_insert_existing_genre(genre_dao, db_connection):
    """Test l'insertion d'un genre existant"""
    test_genre = Genre(id=28, name="Test Genre")

    # Ajouter un genre avec cet ID pour que l'insert échoue
    genre_dao.insert(test_genre)

    # WHEN: Tenter de réinsérer le même genre
    genre_dao.insert(test_genre)

    # THEN: Vérification que le genre n'a pas été ajouté une seconde fois
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM genre WHERE id_genre = %s;", (28,))
        result = cursor.fetchone()

    # Vérification que le genre n'a pas été dupliqué
    assert result[0] == 1, "Genre should exist only once in the database"

    # Nettoyage : supprimer le genre inséré
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM genre WHERE id_genre = %s;", (28,))
        db_connection.commit()

