# la bonne pratique est d'utiliser unschéma réplique de notre base de donnée.
# permet d'éviter que quand on test ajout ça ajoute dans notre vrai bdd.

import os
import pytest
from unittest.mock import patch, MagicMock
from src.DAO.db_connection import DBConnection 

@pytest.fixture
def mock_db_connection(mocker):
    """Fixture pour simuler la connexion à la base de données."""
    # Configuration de l'environnement de test pour utiliser le schéma projet_info_test
    os.environ["host"] = "localhost"
    os.environ["port"] = "5432"
    os.environ["dbname"] = "test_db"
    os.environ["user"] = "test_user"
    os.environ["password"] = "test_password"
    os.environ["pro"] = "projet_info_test"  
    os.environ["test"] = "projet_info_test"  

    # Simule une connexion de base de données
    mock_connect = mocker.patch('src.DAO.db_connection.psycopg2.connect', return_value=MagicMock())
    mock_connection = mock_connect.return_value

    # Retourne une instance de DBConnection pour les tests
    return DBConnection(test=True), mock_connection


def test_initialization(mock_db_connection):
    db_connection, mock_connection = mock_db_connection()
    assert db_connection.connection == mock_connection


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
        unittest.mock.call("CREATE TABLE IF NOT EXISTS MovieMaker (id_movie_maker SERIAL PRIMARY KEY, adult BOOLEAN NOT NULL DEFAULT FALSE, name VARCHAR(255) NOT NULL, gender INTEGER NOT NULL, biography TEXT NOT NULL, birthday DATE, place_of_birth VARCHAR(255), deathday DATE, known_for_department VARCHAR(255), popularity FLOAT NOT NULL, known_for JSONB);"),
        unittest.mock.call("CREATE TABLE IF NOT EXISTS users (id_user SERIAL PRIMARY KEY, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) UNIQUE NOT NULL, hashed_password VARCHAR(255) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL);")
    ]
    
    cursor_mock.execute.assert_has_calls(calls, any_order=True)
    mock_connection.commit.assert_called_once()


def test_insert(mock_db_connection):
    db_connection, mock_connection = mock_db_connection
    test_table = 'users'
    test_values = ('John', 'Doe', 'john_doe', 'hashed_password', 'john@example.com')

    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [{'column_name': 'first_name'}, {'column_name': 'last_name'}, {'column_name': 'username'}, {'column_name': 'hashed_password'}, {'column_name': 'email'}]

    db_connection.insert(test_table, test_values)

    cursor_mock.execute.assert_called_once()
    mock_connection.commit.assert_called_once()

