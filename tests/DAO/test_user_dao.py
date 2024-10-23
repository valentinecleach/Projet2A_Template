from unittest.mock import MagicMock, patch

import pytest

from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class TestUserDao:

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
    def user_dao(self):
        return UserDao()

    # Test INSERT
    def test_insert_user(self, mock_db_connection, user_dao):
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

        # Appeler la méthode d'insertion
        user = user_dao.insert(**new_user)

        # Vérifier que l'utilisateur a été inséré avec les bonnes valeurs
        assert user.username == new_user["username"]
        assert user.phone_number == new_user["phone_number"]

    # Test GET_USER_BY_ID
    def test_get_user_by_id(self, mock_db_connection, user_dao):
        # Simuler le retour de la base de données pour un utilisateur spécifique
        mock_db_connection.fetchone.return_value = {
            "id_user": 1000,
            "username": "JohnDoe",
            "hashed_password": "hashed_password123",
            "date_of_birth": "1990-01-01",
            "gender": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john@example.com",
            "token": "token123",
            "phone_number": "123456789",
        }

        # Appeler la méthode
        user = user_dao.get_user_by_id(1)

        # Vérifier les valeurs renvoyées
        assert user.username == "JohnDoe"
        assert user.email_address == "john@example.com"

    # Test GET_USER_BY_NAME
    def test_get_user_by_name(self, mock_db_connection, user_dao):
        # Simuler le retour de plusieurs utilisateurs par nom
        mock_db_connection.fetchmany.return_value = [
            {
                "id_user": 1,
                "username": "JohnDoe",
                "hashed_password": "hashed_password123",
                "date_of_birth": "1990-01-01",
                "gender": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email_address": "john@example.com",
                "token": "token123",
                "phone_number": "123456789",
            }
        ]

        # Appeler la méthode
        users = user_dao.get_user_by_name("John", size=1)

        # Vérifier le nombre d'utilisateurs retournés
        assert len(users) >= 1
        assert users[0].username == "JohnDoe"

    # Test GET_ALL_USERS
    def test_get_all_users(self, mock_db_connection, user_dao):
        # Simuler le retour de la base de données pour plusieurs utilisateurs
        mock_db_connection.fetchall.return_value = [
            {
                "id_user": 1,
                "username": "JohnDoe",
                "hashed_password": "hashed_password123",
                "date_of_birth": "1990-01-01",
                "gender": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email_address": "john@example.com",
                "token": "token123",
                "phone_number": "123456709",
            }
        ]

        # Appeler la méthode
        users = user_dao.get_all_users(limit=2)

        # Vérifier que deux utilisateurs ont été retournés
        assert len(users) >= 1
        assert users[0].username == "JohnDoe"

    # Test UPDATE_USER
    def test_update_user(self, mock_db_connection, user_dao):
        # Simuler la mise à jour réussie
        mock_db_connection.execute.return_value = 1

        # Appeler la méthode de mise à jour
        user_dao.update_user(
            id_user=1, last_name="JohnUpdated", first_name="updated_john@"
        )

        assert UserDao().get_user_by_id(1).last_name == "JohnUpdated"

    # Test DELETE_USER
    def test_delete_user(self, mock_db_connection, user_dao):
        # Simuler la suppression réussie
        mock_db_connection.execute.return_value = 1

        # Appeler la méthode de suppression
        user_dao.delete_user(1)

        # Vérifier que la requête SQL a bien été exécutée
        assert UserDao().get_user_by_id(1) is None
