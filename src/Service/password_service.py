import hashlib
import secrets
from typing import Optional

# DAO
from src.DAO.user_dao import UserDao

# Model
from src.Model.user import User
from src.Model.connected_user import ConnectedUser

#hash password and salt password in user_service

def hash_password(password:str) -> str:
    """
    """
    pass

def check_password_strenght(password: str):
    """
    """
    if len(password) < 8:
        raise Exception("Password length must be at least 8 characters")
    number = False:
    for i in password:
        if isinstance(i, int): 
            number = True
    if number = False
    

def validate_username_password(username: str, password: str, user_dao: UserDao) -> User:
    connected_user: Optional[User] = user_dao.get_user_by_name(username=username)
    ## TODO

    return connected_user