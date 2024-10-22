from unittest.mock import MagicMock, patch

import pytest

from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


@pytest.fixture
def mock_db():
    with patch('src.DAO.db_connection.DBConnection') as mock_db_conn:
        mock_connection = mock_db_conn.return_value
        mock_cursor = MagicMock()
        mock_connection.connection.cursor.return_value.__enter__.return_value = mock_cursor
        yield mock_cursor

@pytest.fixture
def user_dao():
    return UserDao()

# Test INSERT
def test_insert_user(mock_db, user_dao):
    # Mock the database insertion result
    mock_db.execute.return_value = 1000
    mock_db.fetchone.return_value = None

    # Sample input data for user insertion
    new_user = {
        'id_user': 1000,
        'name': 'John Doe',
        'phone_number': '123456080',
        'email': 'john@exampI.com',
        'gender': 1,
        'date_of_birth': '1990-01-01',
        'hashed_password': 'password123',
        'pseudo': 'johnny'
    }

    # Call the method
    user = user_dao.insert(**new_user)

    # Assertions
    assert user.name == new_user['name']
    assert user.email == new_user['email']

# Test get_user_by_id
def test_get_user_by_id(mock_db, user_dao):
    # Mock the database return value
    mock_db.fetchone.return_value = {
        'id_user': 1,
        'name': 'John Doe',
        'pseudo': 'johnny',
        'email': 'john@example.com',
        'hashed_password': 'password123',
        'date_of_birth': '1990-01-01',
        'phone_number': '123456789',
        'gender': 1
    }

    # Call the method
    user = user_dao.get_user_by_id(1)

    # Assertions
    assert user.name == 'John Doe'
    assert user.email == 'john@example.com'

# Test get_user_by_name
def test_get_user_by_name(mock_db, user_dao):
    # Mock the database return value
    mock_db.fetchmany.return_value = [
        {
            'id_user': 1,
            'name': 'John Doe',
            'pseudo': 'johnny',
            'email': 'john@example.com',
            'hashed_password': 'password123',
            'date_of_birth': '1990-01-01',
            'phone_number': '123456789',
            'gender': 1
        }
    ]

    # Call the method
    users = user_dao.get_user_by_name('John', size=1)

    # Assertions
    assert len(users) == 1
    assert users[0].name == 'John Doe'

# Test get_all_users
def test_get_all_users(mock_db, user_dao):
    # Mock the database return value
    mock_db.fetchall.return_value = [
        {
            'id_user': 1,
            'name': 'John Doe',
            'pseudo': 'johnny',
            'email': 'john@example.com',
            'hashed_password': 'password123',
            'date_of_birth': '1990-01-01',
            'phone_number': '123456789',
            'gender': 1
        },
        {
            'id_user': 2,
            'name': 'Jane Doe',
            'pseudo': 'jane',
            'email': 'jane@example.com',
            'hashed_password': 'password456',
            'date_of_birth': '1992-02-02',
            'phone_number': '987654321',
            'gender': 2
        }
    ]

    # Call the method
    users = user_dao.get_all_users(limit=2)

    # Assertions
    assert len(users) == 2
    assert users[0].name == 'John Doe'
    assert users[1].name == 'Jane Doe'
# Test update_user
def test_update_user(mock_db, user_dao):
    # Mock the database update success
    mock_db.execute.return_value = 1

    # Call the method to update the user
    user_dao.update_user(
        id_user=1,
        name='John Updated',
        email='updated_john@example.com'
    )

    # Assertions
    mock_db.execute.assert_called_once()
    assert 'name = %s' in mock_db.execute.call_args[0][0]
    assert 'email = %s' in mock_db.execute.call_args[0][0]

# Test delete_user
def test_delete_user(mock_db, user_dao):
    # Mock the database deletion success
    mock_db.execute.return_value = 1

    # Call the method
    user_dao.delete_user(1)

    # Assertions
    mock_db.execute.assert_called_once()
    assert 'DELETE' in mock_db.execute.call_args[0][0]
    assert 'id_user = %s' in mock_db.execute.call_args[0][0]
