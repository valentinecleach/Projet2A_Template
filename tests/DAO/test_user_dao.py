import unittest
from unittest.mock import patch, MagicMock
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser

class TestUserDao(unittest.TestCase):

    @patch('src.DAO.db_connection.DBConnection')
    def setUp(self, MockDBConnection):
        self.mock_db_connection = MockDBConnection.return_value
        self.mock_cursor = self.mock_db_connection.connection.cursor.return_value
        self.user_dao = UserDao(self.mock_db_connection)

    def test_insert(self):
        self.mock_cursor.fetchone.return_value = None  # Simulate no existing user
        self.mock_cursor.execute.return_value = None

        user = self.user_dao.insert(1, 'testuser', 'hashed_password', '1990-01-01', 1, 'Test', 'User', 'test@example.com', 'token123')

        self.mock_cursor.execute.assert_called_once()
        self.mock_db_connection.connection.commit.assert_called_once()
        self.assertIsInstance(user, ConnectedUser)

    def test_get_user_by_id(self):
        self.mock_cursor.fetchone.return_value = {
            'id_user': 1,
            'username': 'testuser',
            'hashed_password': 'hashed_password',
            'date_of_birth': '1990-01-01',
            'gender': 1,
            'first_name': 'Test',
            'last_name': 'User',
            'email_address': 'test@example.com',
            'token': 'token123',
            'phone_number': '1234567890'
        }

        user = self.user_dao.get_user_by_id(1)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id_user = %s", (1,))
        self.assertIsInstance(user, ConnectedUser)
        self.assertEqual(user.id_user, 1)

    def test_get_user_by_name(self):
        self.mock_cursor.fetchmany.return_value = [
            {
                'id_user': 1,
                'username': 'testuser',
                'hashed_password': 'hashed_password',
                'date_of_birth': '1990-01-01',
                'gender': 1,
                'first_name': 'Test',
                'last_name': 'User',
                'email_address': 'test@example.com',
                'token': 'token123',
                'phone_number': '1234567890'
            }
        ]

        users = self.user_dao.get_user_by_name('test')

        self.mock_cursor.execute.assert_called_once()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], ConnectedUser)

    def test_get_all_users(self):
        self.mock_cursor.fetchall.return_value = [
            {
                'id_user': 1,
                'username': 'testuser',
                'hashed_password': 'hashed_password',
                'date_of_birth': '1990-01-01',
                'gender': 1,
                'first_name': 'Test',
                'last_name': 'User',
                'email_address': 'test@example.com',
                'token': 'token123',
                'phone_number': '1234567890'
            }
        ]

        users = self.user_dao.get_all_users()

        self.mock_cursor.execute.assert_called_once()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertIsInstance(users[0], ConnectedUser)

    def test_update_user(self):
        self.mock_cursor.execute.return_value = None

        result = self.user_dao.update_user(1, username='updateduser')

        self.mock_cursor.execute.assert_called_once()
        self.mock_db_connection.connection.commit.assert_called_once()
        self.assertEqual(result, 1)

    def test_delete_user(self):
        self.mock_cursor.execute.return_value = None

        result = self.user_dao.delete_user(1)

        self.mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE id_user = %s", (1,))
        self.mock_db_connection.connection.commit.assert_called_once()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
