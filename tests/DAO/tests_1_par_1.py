from unittest.mock import MagicMock, patch

import pytest

from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser
from src.DAO.db_connection import DBConnection
from src.DAO.user_dao import UserDao



class TestUserDao():

    # Fixture pour mocker toute la connexion DB
    @pytest.fixture
    def mock_db_connection(self):
        with patch("src.DAO.db_connection.DBConnection") as mock_db_conn:
            mock_connection = MagicMock()
            mock_cursor = MagicMock()

            # Simulation de la connexion et du curseur
            mock_db_conn.return_value.connection = mock_connection
            mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
            mock_connection.commit = MagicMock()
            mock_connection.rollback = MagicMock()

            yield mock_cursor  # On renvoie le curseur mocké
    
    @pytest.fixture
    def user_dao(self, mock_db_connection):
        return UserDao(mock_db_connection)
         
    def test_insert_user(self, mock_db_connection, user_dao):
        """test la méthode insert_user"""
        # GIVEN
        # Simuler l'insertion réussie
        mock_db_connection.execute.return_value = 1
        mock_db_connection.fetchone.return_value = None

        # Données d'entrée pour l'insertion d'un nouvel utilisateur
        new_user = {
            "id_user": 1,
            "username": "JacDac",
            "hashed_password": "hashed_password123",
            "date_of_birth": "1990-01-01",
            "gender": 1,
            "first_name": "Jac",
            "last_name": "Dac",
            "email_address": "jac@example.com",
            "token": "token123",
            "phone_number": "123456789",
        }

        # WHEN
        # Appeler la méthode d'insertion
        user = user_dao.insert(**new_user)

        # THEN
        # Vérifier que l'utilisateur a été inséré avec les bonnes valeurs
        assert user.username == new_user["username"]
        assert user.phone_number == new_user["phone_number"]

