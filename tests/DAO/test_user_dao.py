from unittest.mock import MagicMock, patch

import pytest

from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


@pytest.fixture
def mock_db():
    with patch("src.DAO.db_connection.DBConnection") as mock_db_conn:
        mock_connection = mock_db_conn.return_value
        mock_cursor = MagicMock()
        # Simulation du retour du curseur avec le mock
        mock_connection.connection.cursor.return_value.__enter__.return_value = (
            mock_cursor
        )
        yield mock_cursor


@pytest.fixture
def user_dao():
    return UserDao()


# Test INSERT
def test_insert_user(mock_db, user_dao):
    # Simuler l'insertion réussie
    mock_db.execute.return_value = 1  # Simuler que 1 ligne est affectée
    mock_db.fetchone.return_value = None

    # Données d'entrée pour l'insertion d'un nouvel utilisateur
    new_user = {
        "id_user": 1000,
        "name": "John Doe",
        "phone_number": "123456789",
        "email": "john@example.com",
        "gender": 1,
        "date_of_birth": "1990-01-01",
        "password": "hashed_password123",
        "pseudo": "johnny",
    }

    # Appeler la méthode d'insertion
    user = user_dao.insert(**new_user)

    # Vérifier que l'utilisateur a été inséré avec les bonnes valeurs
    assert user.name == new_user["name"]
    assert user.email == new_user["email"]

    # Vérifier que l'exécution de la requête a été appelée
    mock_db.execute.assert_called_once()


# Test GET_USER_BY_ID
def test_get_user_by_id(mock_db, user_dao):
    # Simuler le retour de la base de données pour un utilisateur spécifique
    mock_db.fetchone.return_value = {
        "id_user": 1,
        "name": "John Doe",
        "pseudo": "johnny",
        "email": "john@example.com",
        "password": "hashed_password123",
        "date_of_birth": "1990-01-01",
        "phone_number": "123456789",
        "gender": 1,
    }

    # Appeler la méthode
    user = user_dao.get_user_by_id(1)

    # Vérifier les valeurs renvoyées
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

    # Vérifier que la requête SQL a été exécutée
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM user WHERE id_user = %s", (1,)
    )


# Test GET_USER_BY_NAME
def test_get_user_by_name(mock_db, user_dao):
    # Simuler le retour de plusieurs utilisateurs par nom
    mock_db.fetchmany.return_value = [
        {
            "id_user": 1,
            "name": "John Doe",
            "pseudo": "johnny",
            "email": "john@example.com",
            "password": "hashed_password123",
            "date_of_birth": "1990-01-01",
            "phone_number": "123456789",
            "gender": 1,
        }
    ]

    # Appeler la méthode
    users = user_dao.get_user_by_name("John", size=1)

    # Vérifier le nombre d'utilisateurs retournés
    assert len(users) == 1
    assert users[0].name == "John Doe"

    # Vérifier que la requête SQL a été exécutée
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM user WHERE LOWER(name) LIKE %s or LOWER(pseudo) LIKE %s",
        ("%john%", "%john%"),
    )


# Test GET_ALL_USERS
def test_get_all_users(mock_db, user_dao):
    # Simuler le retour de la base de données pour plusieurs utilisateurs
    mock_db.fetchall.return_value = [
        {
            "id_user": 1,
            "name": "John Doe",
            "pseudo": "johnny",
            "email": "john@example.com",
            "password": "hashed_password123",
            "date_of_birth": "1990-01-01",
            "phone_number": "123456789",
            "gender": 1,
        },
        {
            "id_user": 2,
            "name": "Jane Doe",
            "pseudo": "jane",
            "email": "jane@example.com",
            "password": "hashed_password456",
            "date_of_birth": "1992-02-02",
            "phone_number": "987654321",
            "gender": 2,
        },
    ]

    # Appeler la méthode
    users = user_dao.get_all_users(limit=2)

    # Vérifier que deux utilisateurs ont été retournés
    assert len(users) == 2
    assert users[0].name == "John Doe"
    assert users[1].name == "Jane Doe"

    # Vérifier que la requête SQL a été exécutée
    mock_db.execute.assert_called_once_with(
        "SELECT * FROM user WHERE LIMIT 2 OFFSET 0", ()
    )


# Test UPDATE_USER
def test_update_user(mock_db, user_dao):
    # Simuler la mise à jour réussie
    mock_db.execute.return_value = 1  # Une ligne modifiée

    # Appeler la méthode de mise à jour
    user_dao.update_user(
        id_user=1, name="John Updated", email="updated_john@example.com"
    )

    # Vérifier que la requête SQL a bien été exécutée
    mock_db.execute.assert_called_once()
    assert "name = %s" in mock_db.execute.call_args[0][0]
    assert "email = %s" in mock_db.execute.call_args[0][0]


# Test DELETE_USER
def test_delete_user(mock_db, user_dao):
    # Simuler la suppression réussie
    mock_db.execute.return_value = 1  # Une ligne supprimée

    # Appeler la méthode de suppression
    user_dao.delete_user(1)

    # Vérifier que la requête SQL a bien été exécutée
    mock_db.execute.assert_called_once_with("DELETE FROM user WHERE id_user = %s", (1,))
