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

        # Appeler la méthode d'insertion
        user = user_dao.insert(**new_user)

        # Vérifier que l'utilisateur a été inséré avec les bonnes valeurs
        assert user.username == new_user["username"]
        assert user.email_address == new_user["email_address"]

        # Vérifier que la requête SQL a été exécutée avec les bons paramètres
        mock_db_connection.execute.assert_called_once_with(
            "INSERT INTO users(id_user,username,hashed_password,date_of_birth,gender, first_name, last_name,email_address,token,phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                1000,
                "JohnDoe",
                "hashed_password123",
                "1990-01-01",
                1,
                "John",
                "Doe",
                "john@example.com",
                "token123",
                "123456789",
            ),
        )

    # Test GET_USER_BY_ID
    def test_get_user_by_id(self, mock_db_connection, user_dao):
        # Simuler le retour de la base de données pour un utilisateur spécifique
        mock_db_connection.fetchone.return_value = {
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

        # Appeler la méthode
        user = user_dao.get_user_by_id(1)

        # Vérifier les valeurs renvoyées
        assert user.username == "JohnDoe"
        assert user.email_address == "john@example.com"

        # Vérifier que la requête SQL a bien été exécutée avec le bon paramètre
        mock_db_connection.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id_user = %s", (1,)
        )

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
        assert len(users) == 1
        assert users[0].username == "JohnDoe"

        # Vérifier que la requête SQL a bien été exécutée avec les bons paramètres
        mock_db_connection.execute.assert_called_once_with(
            "SELECT * FROM users WHERE LOWER(username) LIKE %s OR LOWER(last_name) LIKE %s OR LOWER(first_name) LIKE %s",
            ("%john%", "%john%", "%john%"),
        )

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
                "phone_number": "123456789",
            },
            {
                "id_user": 2,
                "username": "JaneDoe",
                "hashed_password": "hashed_password456",
                "date_of_birth": "1992-02-02",
                "gender": 2,
                "first_name": "Jane",
                "last_name": "Doe",
                "email_address": "jane@example.com",
                "token": "token456",
                "phone_number": "987654321",
            },
        ]

        # Appeler la méthode
        users = user_dao.get_all_users(limit=2)

        # Vérifier que deux utilisateurs ont été retournés
        assert len(users) == 2
        assert users[0].username == "JohnDoe"
        assert users[1].username == "JaneDoe"

        # Vérifier que la requête SQL a bien été exécutée avec les bons paramètres
        mock_db_connection.execute.assert_called_once_with(
            "SELECT * FROM users LIMIT 2 OFFSET 0", ()
        )

    # Test UPDATE_USER
    def test_update_user(self, mock_db_connection, user_dao):
        # Simuler la mise à jour réussie
        mock_db_connection.execute.return_value = 1

        # Appeler la méthode de mise à jour
        user_dao.update_user(
            id_user=1, username="JohnUpdated", email_address="updated_john@example.com"
        )

        # Vérifier que la requête SQL a bien été exécutée
        mock_db_connection.execute.assert_called_once()
        assert "username = %s" in mock_db_connection.execute.call_args[0][0]
        assert "email_address = %s" in mock_db_connection.execute.call_args[0][0]

    # Test DELETE_USER
    def test_delete_user(self, mock_db_connection, user_dao):
        # Simuler la suppression réussie
        mock_db_connection.execute.return_value = 1

        # Appeler la méthode de suppression
        user_dao.delete_user(1)

        # Vérifier que la requête SQL a bien été exécutée
        mock_db_connection.execute.assert_called_once_with(
            "DELETE FROM users WHERE id_user = %s", (1,)
        )
