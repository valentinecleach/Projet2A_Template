# la bonne pratique est d'utiliser unschéma réplique de notre base de donnée.
# permet d'éviter que quand on test ajout ça ajoute dans notre vrai bdd.

import os
from unittest.mock import MagicMock, patch
from unittest import mock

import pytest
# python -m pip install mock
# python -m pip install pytest-mock
from src.DAO.db_connection import DBConnection



def mock_db_connection(mocker):
    """Fixture pour simuler la connexion à la base de données."""
    # Mock dotenv.load_dotenv pour ne pas lire les infos du .env
    mocker.patch("dotenv.load_dotenv", return_value=None)
    
    # Configuration de l'environnement de test pour utiliser le schéma projet_info_test
    mocker.patch.dict(os.environ, {
        "host": "localhost",
        "port": "5432",
        "dbname": "test_db",
        "user": "test_user",
        "password": "test_password",
        "schema": "projet_info_test"
    }, clear=True) # clear pour bien effacer les variables précédamment dans le test

    mocker.patch(
        "src.DAO.db_connection.psycopg2.connect", return_value=MagicMock()
    )
    
    # Retourne une instance de DBConnection pour les tests
    return DBConnection()


def test_initialization_no_config(mocker):
    # GIVEN / WHEN
    db_connection = mock_db_connection(mocker)

    # THEN
    assert db_connection.host == "localhost" # "sgbd-eleves.domensai.ecole" != "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.schema == "projet_info_test"
    

def test_initialization_config():
    # GIVEN
    config = {
        "host": "localhost",
        "port": "5432",
        "database": "test_db",
        "user": "test_user",
        "password": "test_password",
        "schema": "projet_info_test"
    }

    # WHEN
    db = DBConnection(config=config)

    # THEN
    assert db.host == "localhost"
    assert db.port == "5432"
    assert db.database == "test_db"
    assert db.user == "test_user"
    assert db.password == "test_password"
    assert db.schema == "projet_info_test"


def test_set_search_path(mock_db_connection):
    db_connection, mock_connection = mock_db_connection
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    db_connection._DBConnection__set_search_path("projet_info_test")

    cursor_mock.execute.assert_called_once_with("SET search_path TO projet_info_test;")
    mock_connection.commit.assert_called_once()


def test_create_tables(mock_db_connection):
    db_connection, mock_connection = mock_db_connection
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
   
    db_connection.create_tables()

    calls = [
       unittest.mock.call(
          "CREATE TABLE IF NOT EXISTS MovieMaker (id_movie_maker SERIAL PRIMARY KEY, adult BOOLEAN NOT NULL DEFAULT FALSE, name VARCHAR(255) NOT NULL, gender INTEGER NOT NULL, biography TEXT NOT NULL, birthday DATE, place_of_birth VARCHAR(255), deathday DATE, known_for_department VARCHAR(255), popularity FLOAT NOT NULL, known_for JSONB);"
       ),
        unittest.mock.call(
            "CREATE TABLE IF NOT EXISTS users (id_user SERIAL PRIMARY KEY, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) UNIQUE NOT NULL, hashed_password VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL);"
        ),
    ]

    cursor_mock.execute.assert_has_calls(calls, any_order=True)
    mock_connection.commit.assert_called_once()


def test_insert(mock_db_connection):
    db_connection, mock_connection = mock_db_connection
    test_table = "users"
    test_values = ("John", "Doe", "john_doe", "hashed_password", "john@example.com")
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        {"column_name": "first_name"},
        {"column_name": "last_name"},
        {"column_name": "username"},
        {"column_name": "hashed_password"},

        {"column_name": "email"},
    ]
    
    db_connection.insert(test_table, test_values)

    cursor_mock.execute.assert_called_once()
    mock_connection.commit.assert_called_once()
