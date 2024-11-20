# pip install bcrypt
import bcrypt
import pytest
import hashlib

from src.Service.password_service import (check_password_strenght, create_salt, hash_password)

#python -m pytest tests/Service/test_password_service.py

# Test du hashage de mot de passe
def test_hash_password_no_salt():
    password = "NoCode"
    hashed_password = hash_password(password)
    assert hashed_password == "9da90a168c5026a3291f7612de2caebc7e36ae4c630416fc3332a41a1c630fee"

def test_hash_password_with_salt():
    password = "NoCode"
    salt = ["tes", "tuser", "2"]
    hashed_password = hash_password(password, salt)
    assert hashed_password == "d9812273fc89e21a4840370fad863191e476a08d4caa36dcd33a82f4fc4b9cdb"


# Test de la création de sel sans token
def test_create_salts():
    # GIVEN
    username = "testuser"
    user_password_token = "123456"
    # When
    salt = create_salt(username, user_password_token)

    # THEN
    assert len(salt) == 3  # Le sel doit être composé de 2 parties
    assert salt[0] == "tes"  # Les trois premiers caractères du username
    assert salt[1] == "tuser123456"   # Les caractères restants du username + le token


# Test de la vérification de la force du mot de passe
def test_check_password_strenght_valid():
    valid_password = "Password1"

    # Si le mot de passe est valide, aucune exception ne doit être levée
    try:
        check_password_strenght(valid_password)
    except Exception:
        pytest.fail("Password should be strong enough")


def test_check_password_strenght_invalid_length():
    short_password = "Pass1"

    # Le mot de passe est trop court, une exception doit être levée
    with pytest.raises(Exception) as exc_info:
        check_password_strenght(short_password)
    
    assert str(exc_info.value) == "Password length must be at least 8 characters"


def test_check_password_strenght_invalid_number():
    no_number_password = "Password"

    # Le mot de passe n'a pas de chiffre, une exception doit être levée
    with pytest.raises(Exception) as exc_info:
        check_password_strenght(no_number_password)
    
    assert str(exc_info.value) == "Password must contain at least one number"
