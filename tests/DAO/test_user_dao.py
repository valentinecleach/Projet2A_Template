import unittest
from unittest.mock import MagicMock, patch

from src.DAO.db_connection import DBConnection
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class TestUserDao(unittest.TestCase):
    
    def setUp(self):
        # Setup initial conditions for tests
        self.user_dao = UserDao()

    # Test for the insert method
    @patch('DBConnection.insert')
    def test_insert_user(self, mock_insert):
        mock_insert.return_value = True
        
        user = self.user_dao.insert(
            id_user=1,
            name="John Doe",
            phone_number="1234567890",
            email="johndoe@example.com",
            gender=1,
            date_of_birth="1990-01-01",
            password="password123",
            pseudo="jdoe"
        )

        self.assertIsInstance(user, ConnectedUser)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.gender, 1)

    # Test for the get_user_by_id method
    @patch('DBConnection.read_by_id')
    def test_get_user_by_id(self, mock_read_by_id):
        mock_read_by_id.return_value = {
            "name": "John Doe",
            "pseudo": "jdoe",
            "email": "johndoe@example.com",
            "password": "password123",
            "date_of_birth": "1990-01-01",
            "phone_number": "1234567890"
        }

        user = self.user_dao.get_user_by_id(1)
        
        self.assertIsInstance(user, ConnectedUser)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "johndoe@example.com")

    # Test for the get_user_by_name method
    @patch('DBConnection.read_by_string')
    def test_get_user_by_name(self, mock_read_by_string):
        mock_read_by_string.return_value = [
            {
                "name": "John Doe",
                "pseudo": "jdoe",
                "email": "johndoe@example.com",
                "gender": 1,
                "password": "password123",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            }
        ]

        users = self.user_dao.get_user_by_name("John", size=10)
        
        self.assertEqual(len(users), 1)
        self.assertIsInstance(users[0], ConnectedUser)
        self.assertEqual(users[0].name, "John Doe")

    # Test for the get_all_users method
    @patch('DBConnection.read_all')
    def test_get_all_users(self, mock_read_all):
        mock_read_all.return_value = [
            {
                "name": "John Doe",
                "pseudo": "jdoe",
                "email": "johndoe@example.com",
                "gender": 1,
                "password": "password123",
                "date_of_birth": "1990-01-01",
                "phone_number": "1234567890"
            },
            {
                "name": "Jane Smith",
                "pseudo": "jsmith",
                "email": "janesmith@example.com",
                "gender": 2,
                "password": "password456",
                "date_of_birth": "1992-02-02",
                "phone_number": "0987654321"
            }
        ]

        users = self.user_dao.get_all_users(limit=2, offset=0)
        
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "John Doe")
        self.assertEqual(users[1].name, "Jane Smith")

    # Test for the update_user method
    @patch('DBConnection.connection')
    def test_update_user(self, mock_db_conn):
        mock_cursor = MagicMock()
        mock_db_conn.cursor.return_value.__enter__.return_value = mock_cursor

        self.user_dao.update_user(
            id_user=1,
            name="John Updated",
            email="johnupdated@example.com"
        )

        mock_cursor.execute.assert_called_once()
        self.assertTrue(mock_cursor.execute.called)

    # Test for the delete_user method
    @patch('DBConnection.delete')
    def test_delete_user(self, mock_delete):
        mock_delete.return_value = True

        self.user_dao.delete_user(1)
        mock_delete.assert_called_with('cine.user', 'id_user', 1)



if __name__ == '__main__':
    unittest.main()
