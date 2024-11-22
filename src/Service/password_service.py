import hashlib
import secrets
from typing import List, Optional

import bcrypt

# DAO
# from src.DAO.user_dao import UserDao
# from src.Model.connected_user import ConnectedUser

# Model
# from src.Model.user import User

# hash password and salt password in user_service


def hash_password(password: str, salt: Optional[List[str]] = None) -> str:
    """Hashes the password. The salt is optional

    parameters
    ----------
    password: str
        password enter by the user
    salt: list
        generate a square hash

    """
    if salt is None:
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    else:
        salted_password = f"{salt[0]}{password}{salt[1]}".encode("utf-8")
        hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password


def create_salt(username: str, user_password_token: Optional[str] = None) -> list[str]:
    """Creates a salt for the password to be hashed
    
    parameters
    ----------
    username: str
    user_password_token: str
        the token of the password 
    """
    # Création des parties de sel
    password_token = (
        user_password_token if user_password_token else secrets.token_hex(16)
    )
    start_salt = username[:3]  # Les trois premiers caractères du nom d'utilisateur
    end_salt = (
        username[3:] + password_token
    )  # Les caractères restants du nom d'utilisateur et la clef secrete.
    return [start_salt, end_salt, password_token]


def verify_password(username, password_tried, user_password_token, hashed_password):
    "verify the password"
    salt = create_salt(username, user_password_token)
    hashed_password_tried = hash_password(password=password_tried, salt=salt)
    return hashed_password_tried == hashed_password


def check_password_strenght(password: str):
    """Checks a passwords strenght.
    If the password is not strong enough (too short, not enough characters etc), an exception wil be raised

    Parameters
    ----------
    password : str
        The password
    """
    if len(password) < 8:
        raise ValueError("Password length must be at least 8 characters")
    number = False
    for char in password:
        if char.isdigit():
            number = True
    if number is False:
        raise ValueError("Password must contain at least one number")


# def validate_username_password(username: str, password: str, user_dao: UserDao) -> User:
#    connected_user: Optional[User] = user_dao.get_user_by_name(username=username)
## Fait dans user_service donc pas nécéssaire?
#    return connected_user
