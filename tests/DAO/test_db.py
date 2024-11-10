# la bonne pratique est d'utiliser unschéma réplique de notre base de donnée.
# permet d'éviter que quand on test ajout ça ajoute dans notre vrai bdd.

import os
from unittest.mock import MagicMock, patch
from unittest import mock
import unittest

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

    mock_connection = MagicMock()
    mocker.patch(
        "src.DAO.db_connection.psycopg2.connect", return_value=mock_connection
    )
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Set up the mock cursor's behavior for execute, fetchone, and fetchall
    mock_cursor.execute = MagicMock()
    
    # Retourne une instance de DBConnection pour les tests
    mock_connection = DBConnection()
    return mock_connection, mock_cursor


def test_initialization_no_config(mocker):
    """On teste l'initiatlisation si l'attribut config n'est pas donné
    """
    # GIVEN / WHEN
    db_connection, mock_cursor = mock_db_connection(mocker)

    # THEN
    assert db_connection.host == "localhost" # "sgbd-eleves.domensai.ecole" != "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.schema == "projet_info_test"
    

def test_initialization_config():
    """On teste l'initiatlisation si l'attribut config est donné
    """
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
    db_connection = DBConnection(config=config)

    # THEN
    assert db_connection.host == "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.schema == "projet_info_test"

# pas de methode set search path? Pq on a ce
def test_set_search_path(mocker):
    """SVP ajoutez de la docu pour qu'on puisse comprendre qqe chose. Merci :)
    """
    mock_connection, mock_cursor = mock_db_connection(mocker)

    mock_connection._DBConnection__set_search_path("projet_info_test")

    mock_cursor.execute.assert_called_once_with("SET search_path TO projet_info_test;")
    mock_connection.commit.assert_called_once()


def test_create_tables(mocker):
    """ Teste la création de tables avec la méthode sql_query
    """
    # GIVEN
    mock_connection, mock_cursor = mock_db_connection(mocker)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS test_table_MovieMaker( 
        id_movie_maker SERIAL PRIMARY KEY, 
        adult BOOLEAN NOT NULL DEFAULT FALSE, 
        name VARCHAR(255) NOT NULL, 
        gender INTEGER NOT NULL, 
        biography TEXT NOT NULL, 
        birthday DATE, 
        place_of_birth VARCHAR(255), 
        deathday DATE, 
        known_for_department VARCHAR(255), 
        popularity FLOAT NOT NULL, 
        known_for JSONB);
    """

    # WHEN
    mock_connection.sql_query(create_table_query)

    #calls = [
    #   unittest.mock.call(
    #      "CREATE TABLE IF NOT EXISTS MovieMaker (id_movie_maker SERIAL PRIMARY KEY, adult BOOLEAN NOT NULL DEFAULT FALSE, name VARCHAR(255) NOT NULL, gender INTEGER NOT NULL, biography TEXT NOT NULL, birthday DATE, place_of_birth VARCHAR(255), deathday DATE, known_for_department VARCHAR(255), popularity FLOAT NOT NULL, known_for JSONB);"
    #   ),
    #    unittest.mock.call(
    #        "CREATE TABLE IF NOT EXISTS users (id_user SERIAL PRIMARY KEY, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) UNIQUE NOT NULL, hashed_password VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL);"
    #    ),
    #]
    calls = unittest.mock.call(create_table_query, None)

    # THEN: Verify the calls were made to execute
    mock_cursor.execute.assert_has_calls(calls, any_order=True)

    mock_connection.commit.assert_called_once()


def test_insert(mock_db_connection):
    """Teste
    """
    mock_connection, mock_cursor = mock_db_connection(mocker)

    test_table = "users"
    test_values = ("John", "Doe", "john_doe", "hashed_password", "john@example.com")
    mock_cursor.fetchall.return_value = [
        {"column_name": "first_name"},
        {"column_name": "last_name"},
        {"column_name": "username"},
        {"column_name": "hashed_password"},
        {"column_name": "email"},
    ]
    
    db_connection.insert(test_table, test_values)

    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_called_once()
