# la bonne pratique est d'utiliser unschéma réplique de notre base de donnée.
# permet d'éviter que quand on test ajout ça ajoute dans notre vrai bdd.

import os
import unittest
from typing import Literal, Optional, Union
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

# python -m pip install mock
# python -m pip install pytest-mock
from src.DAO.db_connection import DBConnector

# python -m pytest tests_directory/foo.py tests_directory/bar.py -k 'test_001'
# python -m pytest tests/DAO/test_db.py -k 'test_initialization_no_config'


def mock_db_connection(mocker):
    """Fixture pour simuler la connexion à la base de données."""
    # Mock dotenv.load_dotenv pour ne pas lire les infos du .env
    mocker.patch("dotenv.load_dotenv", return_value=None)

    # Configuration de l'environnement de test pour utiliser le schéma projet_info_test
    mocker.patch.dict(
        os.environ,
        {
            "host": "localhost",
            "port": "5432",
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_password",
            "schema": "projet_info_test",
        },
        clear=True,
    )  # clear pour bien effacer les variables précédamment dans le test

    mock_connection = MagicMock()
    mocker.patch("src.DAO.db_connection.psycopg2.connect", return_value=mock_connection)
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    # Set up the mock cursor's behavior for execute, fetchone, and fetchall
    mock_cursor.execute = MagicMock()

    # Retourne une instance de DBConnection pour les tests
    mock_connection = DBConnector()
    return mock_connection, mock_cursor


# OK
def test_initialization_no_config(mocker):
    """On teste l'initiatlisation si l'attribut config n'est pas donné"""
    # GIVEN / WHEN
    db_connection, mock_cursor = mock_db_connection(mocker)

    # THEN
    assert (
        db_connection.host == "localhost"
    )  # "sgbd-eleves.domensai.ecole" != "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.schema == "projet_info_test"


# python -m pytest tests/DAO/test_db.py -k 'test_initialization_config'
# OK
def test_initialization_config():
    """On teste l'initiatlisation si l'attribut config est donné"""
    # GIVEN
    config = {
        "host": "localhost",
        "port": "5432",
        "database": "test_db",
        "user": "test_user",
        "password": "test_password",
        "schema": "projet_info_test",
    }

    # WHEN
    db_connection = DBConnector(config=config)

    # THEN
    assert db_connection.host == "localhost"
    assert db_connection.port == "5432"
    assert db_connection.database == "test_db"
    assert db_connection.user == "test_user"
    assert db_connection.password == "test_password"
    assert db_connection.schema == "projet_info_test"


# MockDBConnection (for DAO tests and MovieService)
class MockDBConnection:
    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "one",
    ):
        match query:
            case "SELECT * from users WHERE id=%s":
                if not data:
                    raise Exception
                id_user = data[0]
                return {
                    "id": id_user,
                    "username": "janjak",
                    "password": "myHashedPassword",
                    "salt": "mySalt",
                }


def test_insert(mocker):
    """Teste la création de tables avec la méthode sql_query"""
    # GIVEN
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
    insert_table_query = """ 
    INSERT ;
    """

    # WHEN
    mock_connection.sql_query(insert_table_query)

    # GIVEN

