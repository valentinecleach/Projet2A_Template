import bcrypt
import pytest

from src.Service.password_service import (check_password_strenght, create_salt,
                                          create_token, hash_password)


# Test du hashage de mot de passe
def test_hash_password():
    password = "strongpassword123"
    username = "testuser"
    token = create_token(username)
    salt = create_salt(username, token)

    hashed_password = hash_password(password, salt)

    # Vérification que le mot de passe a bien été haché
    assert bcrypt.checkpw(f"{salt[0]}{password}{salt[1]}".encode('utf-8'), hashed_password) is True


# Test de la création de sel
def test_create_salt():
    username = "testuser"
    token = create_token(username)
    salt = create_salt(username, token)

    assert len(salt) == 2  # Le sel doit être composé de 2 parties
    assert salt[0] == "tes"  # Les trois premiers caractères du username
    assert salt[1] == "tuser" + token  # Les caractères restants du username + le token


# Test de la création de token
def test_create_token():
    username = "testuser"
    token = create_token(username)

    assert isinstance(token, str)
    assert len(token) == 32  # Un token hexadécimal de 16 bytes génère une chaîne de 32 caractères


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
