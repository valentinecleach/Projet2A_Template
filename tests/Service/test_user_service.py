from datetime import date

import pytest

from src.DAO.db_connection import DBConnector
from src.Service.user_service import UserService


@pytest.fixture
def db_connection():
    """Fixture pour fournir une connexion à la base de données."""
    return DBConnector()


@pytest.fixture
def user_service(db_connection):
    """Fixture pour initialiser le UserService."""
    return UserService(db_connection)


def test_check_valid_username(user_service):
    """Teste la validation d'un nom d'utilisateur."""
    valid_username = "new_user"
    user_service.check_valid_username(
        valid_username
    )  # Ne devrait pas lever d'exception

    invalid_username = "abc"
    with pytest.raises(ValueError, match="Username must contain at least 5 characters"):
        user_service.check_valid_username(invalid_username)


def test_sign_up(user_service):
    """Teste l'inscription d'un utilisateur."""
    username = "test_user1"
    user_service.sign_up(
        first_name="Test",
        last_name="User",
        username=username,
        password="StrongPassword123!",
        gender=1,
        date_of_birth=date(1990, 1, 1),
        email_address="testuser@example.com",
        phone_number="1234567890",
    )
    # Vérifie que l'utilisateur est dans la base
    user = user_service.user_dao.get_user_by_name(username)
    assert user is not None
    assert user[0].username == username


def test_sign_up_duplicate_username(user_service):
    """Teste l'inscription avec un nom d'utilisateur déjà existant."""
    username = "duplicate_user"
    user_service.sign_up(
        first_name="Duplicate",
        last_name="User",
        username=username,
        password="StrongPassword123!",
        gender=1,
        date_of_birth=date(1990, 1, 1),
        email_address="duplicateuser@example.com",
    )
    with pytest.raises(ValueError, match="This username is already taken."):
        user_service.sign_up(
            first_name="Duplicate2",
            last_name="User2",
            username=username,
            password="AnotherStrongPassword123!",
            gender=1,
            date_of_birth=date(1992, 2, 2),
            email_address="duplicateuser2@example.com",
        )


def test_log_in(user_service):
    """Teste la connexion avec un utilisateur valide."""
    username = "login_test_user1"
    password = "LoginTestPassword123!"
    user_service.sign_up(
        first_name="Login",
        last_name="TestUser",
        username=username,
        password=password,
        gender=1,
        date_of_birth=date(1990, 1, 1),
        email_address="logintestuser@example.com",
    )
    assert user_service.log_in(username, password) is True


def test_log_in_invalid_user(user_service):
    """Teste la connexion avec un utilisateur invalide."""
    invalid_username = "invalid_user"
    invalid_password = "InvalidPassword123!"
    assert user_service.log_in(invalid_username, invalid_password) is False


def test_log_in_invalid_password(user_service):
    """Teste la connexion avec un mot de passe incorrect."""
    username = "wrong_password_user1"
    correct_password = "CorrectPassword123!"
    user_service.sign_up(
        first_name="WrongPassword",
        last_name="User",
        username=username,
        password=correct_password,
        gender=1,
        date_of_birth=date(1990, 1, 1),
        email_address="wrongpassworduser@example.com",
    )
    assert user_service.log_in(username, "WrongPassword123!") is False


@pytest.fixture(scope="function")
def clean_user_table(db_connection):
    """Fixture pour nettoyer la table des utilisateurs avant chaque test."""
    query = "DELETE FROM users WHERE username = %s"
    db_connection.sql_query(query, ("test_user",), return_type="none")
    db_connection.sql_query(query, ("duplicate_user",), return_type="none")
    db_connection.sql_query(query, ("login_test_user",), return_type="none")
    db_connection.sql_query(query, ("wrong_password_user",), return_type="none")
