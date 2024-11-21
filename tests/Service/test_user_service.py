from datetime import date

import pytest

from src.DAO.db_connection import DBConnector
from src.Service.user_service import UserService


@pytest.fixture
def setup_user_service():
    """Fixture pour configurer UserService avec une connexion à la base de données."""
    db_connection = DBConnector()  # Connexion à la base de données
    user_service = UserService(db_connection)
    return user_service


def test_sign_up(setup_user_service):
    """Test pour vérifier que l'utilisateur peut s'inscrire correctement."""
    user_data = {
        "first_name": "Carmelo",
        "last_name": "Anthony",
        "username": "Lamelo123",
        "password": "SecurePassword123!",
        "gender": 1,  # Exemple de genre (1 pour masculin, 2 pour féminin)
        "date_of_birth": date(1990, 12, 25),
        "email_address": "lamelo123@example.com",
        "phone_number": "123-456-7898",
    }
    # Inscription de l'utilisateur
    user_service = setup_user_service
    user_service.sign_up(**user_data)

    # Vérification que l'utilisateur a été ajouté à la base de données
    user_from_db = user_service.user_dao.get_user_by_name("Lamelo123")

    # Vérification que l'utilisateur existe et a bien les bonnes informations
    assert user_from_db is not None
    assert user_from_db[0].username == "Lamelo123"
    assert user_from_db[0].first_name == "Carmelo"
    assert user_from_db[0].last_name == "Anthony"
    assert user_from_db[0].email_address == "lamelo123@example.com"
    assert user_from_db[0].phone_number == "123-456-7898"
    assert user_from_db[0].date_of_birth == date(1990, 12, 25)


def test_log_in(setup_user_service, capfd):
    """Test pour vérifier que l'utilisateur peut se connecter correctement après s'être inscrit."""
    user_service = setup_user_service

    # Test de connexion avec le bon username et password
    user_service.log_in("jonas1", "SecurePassword123!")

    # Vérification que le message de succès est affiché dans la sortie standard
    captured = capfd.readouterr()
    assert "Utilisateur 'jonas1' connecté avec succès." in captured.out
