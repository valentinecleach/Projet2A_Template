import unittest
from unittest.mock import MagicMock, patch

from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class TestUserDao(unittest.TestCase):

    @patch("src.DAO.db_connection.DBConnection")
    def test_insert(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value

        user_dao = UserDao()
        user = user_dao.insert(
            1,
            "testuser",
            "hashed_password",
            "1990-01-01",
            1,
            "Test",
            "User",
            "test@example.com",
            "token123",
        )

        mock_cursor.execute.assert_called_once()
        mock_conn.connection.commit.assert_called_once()
        self.assertIsInstance(user, ConnectedUser)

    @patch("src.DAO.db_connection.DBConnection")
    def test_get_user_by_id(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value
        mock_cursor.fetchone.return_value = {
            "id_user": 1,
            "username": "testuser",
            "hashed_password": "hashed_password",
            "date_of_birth": "1990-01-01",
            "gender": 1,
            "first_name": "Test",
            "last_name": "User",
            "email_address": "test@example.com",
            "token": "token123",
            "phone_number": "1234567890",
        }

        user_dao = UserDao()
        user = user_dao.get_user_by_id(1)

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM users WHERE id_user = %s", (1,)
        )
        self.assertIsInstance(user, ConnectedUser)
        self.assertEqual(user.id_user, 1)

    @patch("src.DAO.db_connection.DBConnection")
    def test_get_user_by_name(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value
        mock_cursor.fetchmany.return_value = [
            {
                "id_user": 1,
                "username": "testuser",
                "hashed_password": "hashed_password",
                "date_of_birth": "1990-01-01",
                "gender": 1,
                "first_name": "Test",
                "last_name": "User",
                "email_address": "test@example.com",
                "token": "token123",
                "phone_number": "1234567890",
            }
        ]

        user_dao = UserDao()
        users = user_dao.get_user_by_name("test")

        mock_cursor.execute.assert_called_once()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], ConnectedUser)

    @patch("src.DAO.db_connection.DBConnection")
    def test_get_all_users(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {
                "id_user": 1,
                "username": "testuser",
                "hashed_password": "hashed_password",
                "date_of_birth": "1990-01-01",
                "gender": 1,
                "first_name": "Test",
                "last_name": "User",
                "email_address": "test@example.com",
                "token": "token123",
                "phone_number": "1234567890",
            }
        ]

        user_dao = UserDao()
        users = user_dao.get_all_users()

        mock_cursor.execute.assert_called_once()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], ConnectedUser)

    @patch("src.DAO.db_connection.DBConnection")
    def test_update_user(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value

        user_dao = UserDao()
        result = user_dao.update_user(1, username="updateduser")

        mock_cursor.execute.assert_called_once()
        mock_conn.connection.commit.assert_called_once()
        self.assertEqual(result, 1)

    @patch("src.DAO.db_connection.DBConnection")
    def test_delete_user(self, MockDBConnection):
        mock_conn = MockDBConnection.return_value
        mock_cursor = mock_conn.connection.cursor.return_value

        user_dao = UserDao()
        result = user_dao.delete_user(1)

        mock_cursor.execute.assert_called_once_with(
            "DELETE FROM users WHERE id_user = %s", (1,)
        )
        mock_conn.connection.commit.assert_called_once()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
