import hashlib
import secrets
from typing import Optional

# DAO
from src.DAO.user_dao import UserDao

# Model
from src.Model.user import User
from src.Model.connected_user import ConnectedUser

#hash password and salt password in user_service


def check_password_strenght(password: str):
    """ Checks a passwords strenght. 
    If the password is not strong enough (too short, not enough characters etc), an exception wil be raised

    Parameters
    ----------
    password : str
        The password
    """
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")
    length = len(password)
    number = False:
    for i in length:
        if isinstance(password[i-1], int): 
            number = True
    if number = False:
        raise Exception('Password must contain at least one number')
    

def validate_username_password(username: str, password: str, user_dao: UserDao) -> User:
    connected_user: Optional[User] = user_dao.get_user_by_name(username=username)
    ## Fait dans user_service donc pas nécéssaire?
    return connected_user