import hashlib
import secrets
from typing import Optional

# DAO
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser

# Model
from src.Model.user import User

# hash password and salt password in user_service


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Hashes the password"""
    salted_password = f"{salt[0]}{password}{salt[1]}".encode("utf-8")
    hashed_password = bcrypt.hashpw(salted_password, bcrypt.gensalt())
    return hashed_password


def create_salt(username: str) -> list[str]:
    """Creates a salt for the password to be hashed"""
    # Création des parties de sel
    start_salt = username[:3]  # Les trois premiers caractères du nom d'utilisateur
    end_salt = username[3:] + secrets.token_hex(
        16
    )  # Les caractères restants du nom d'utilisateur et une clef secrete.
    salt = [start_user, end_user]


def check_password_strenght(password: str):
    """Checks a passwords strenght.
    If the password is not strong enough (too short, not enough characters etc), an exception wil be raised

    Parameters
    ----------
    password : str
        The password
    """
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")
    length = len(password)
    number = False
    for i in length:
        if isinstance(password[i - 1], int):
            number = True
    if number is False:
        raise Exception("Password must contain at least one number")


#def validate_username_password(username: str, password: str, user_dao: UserDao) -> User:
#    connected_user: Optional[User] = user_dao.get_user_by_name(username=username)
    ## Fait dans user_service donc pas nécéssaire?
#    return connected_user
