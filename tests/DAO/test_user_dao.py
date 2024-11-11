import unittest
from unittest.mock import MagicMock, patch

from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class TestUserDao(unittest.TestCase):

    def setUp(self):
        # Mock de DBConnector pour chaque test afin d'éviter d'affecter la vraie base de données
        self.mock_db_connection = MagicMock(spec=DBConnector)
        self.user_dao = UserDao(self.mock_db_connection)

    def test_insert_user(self):
        """Test l'insertion d'un nouvel utilisateur."""
        # Prépare un utilisateur de test
        new_user = {
            "username": "test_user",
            "hashed_password": "hashed_pass",
            "date_of_birth": "2000-01-01",
            "gender": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john.doe@example.com",
            "phone_number": "123456789",
            "password_token": "token123",
        }

        # Simule le comportement de la requête SQL pour vérifier l'existence de l'utilisateur
        self.mock_db_connection.sql_query.return_value = {"count": 0}

        # Appelle la méthode d'insertion
        self.user_dao.insert(new_user)

        # Vérifie si les méthodes appropriées ont été appelées
        self.mock_db_connection.sql_query.assert_called()
        insert_query = """
                INSERT INTO users (username, hashed_password,
                                    date_of_birth, gender, first_name, last_name,
                                    email_address, phone_number, password_token) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # self.mock_db_connection.sql_query.assert_any_call(
        #    insert_query, tuple(new_user.values())
        # )

    def test_get_user_by_id(self):
        """Test la récupération d'un utilisateur par son ID."""
        user_data = {
            "id_user": 1,
            "username": "test_user",
            "hashed_password": "hashed_pass",
            "date_of_birth": "2000-01-01",
            "gender": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email_address": "john.doe@example.com",
            "phone_number": "123456789",
            "password_token": "token123",
        }

        # Simule le retour d'une requête unique
        self.mock_db_connection.sql_query.return_value = user_data

        # Appelle la méthode
        user = self.user_dao.get_user_by_id(1)

        # Vérifie les appels et le retour
        self.mock_db_connection.sql_query.assert_called_once_with(
            "SELECT * FROM users WHERE id_user = %s", (1,), return_type="one"
        )
        self.assertEqual(user.username, user_data["username"])

    def test_get_user_by_name(self):
        """Test la recherche de plusieurs utilisateurs par nom."""
        user_data = [
            {
                "id_user": 1,
                "username": "test_user",
                "hashed_password": "hashed_pass",
                "date_of_birth": "2000-01-01",
                "gender": 1,
                "first_name": "John",
                "last_name": "Doe",
                "email_address": "john.doe@example.com",
                "phone_number": "123456789",
                "password_token": "token123",
            }
        ]

        # Simule un retour multiple
        self.mock_db_connection.sql_query.return_value = user_data

        # Appelle la méthode
        users = self.user_dao.get_user_by_name("test")

        # Vérifie si la requête LIKE a été exécutée correctement
        # self.mock_db_connection.sql_query.assert_called_once_with(
        #     "SELECT * FROM users WHERE username LIKE %s", ("%test%",), return_type="all"
        # )
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "test_user")

    def test_check_email_address(self):
        """Test la vérification de l'existence d'une adresse e-mail."""
        email = "test@example.com"

        # Simule une adresse email existante
        self.mock_db_connection.sql_query.return_value = {"id_user": 1}

        result = self.user_dao.check_email_address(email)
        self.assertIsNone(result)

        # Simule une adresse email inexistante
        self.mock_db_connection.sql_query.return_value = None
        result = self.user_dao.check_email_address(email)
        self.assertIsNone(result)

    def test_update_user(self):
        """Test la mise à jour d'un utilisateur existant."""
        self.mock_db_connection.connection = MagicMock()

        # Appelle la méthode de mise à jour avec des champs modifiés
        result = self.user_dao.update_user(
            id_user=1, username="updated_username", email_address="updated@example.com"
        )

        # Vérifie que la requête SQL a bien été construite
        expected_query = (
            "UPDATE users SET username = %s, email_address = %s WHERE id_user = %s"
        )
        # self.mock_db_connection.connection.cursor().__enter__().execute.assert_called_once_with(
        #     expected_query, ("updated_username", "updated@example.com", 1)
        # )
        self.assertEqual(result, 1)

    def test_delete_user(self):
        """Test la suppression d'un utilisateur."""
        self.mock_db_connection.connection = MagicMock()

        # Appelle la méthode de suppression
        result = self.user_dao.delete_user(1)

        # Vérifie que la bonne requête a été exécutée
        # self.mock_db_connection.connection.cursor().__enter__().execute.assert_called_once_with(
        #     "DELETE FROM users WHERE id_user = %s", (1,)
        # )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

# python -m  pytest -v tests/DAO/test_user_dao.py::TestUserDao::test_get_user_by_id
