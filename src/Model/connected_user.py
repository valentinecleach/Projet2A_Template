from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.Model.user import User


class ConnectedUser(User):
    """

    Attributes
    ----------
    id_user: int
        the id of th user
    username: str
        the pseudonyme of the user
    hashed_password: str
        the password the user has created after been hashed
    date_of_birth: date
        the date of birth entered by the user
    gender: int
        the gender entered by the user
    first_name: str
        the first name of the user
    last_name: str
        the last name of the user
    email_adress: str
        the email adress of the user
    password_token: str
        object used for password
    phone_number:str
        the phone number of user
    own_film_collection: list
        list of id_movie of favorite movies
    follow_list: list
        list of user_id of user followed
    """
    id_user: int
    username: str
    hashed_password: str
    date_of_birth: date
    gender: int
    first_name: str
    last_name: str
    email_address: str
    password_token: str
    phone_number: str | None = None  
    own_film_collection: list | None = None
    follow_list: list | None = None

    def __str__(self):
        """user information: id and pseudonym """
        return f"id: {self.id_user}, username: {self.username}"

    def __repr__(self):
        """ user information: id, pseudonym and saved lists: movie collection and subscriptions
        """
        return (f"id : {self.id_user}, "
            f"username : {self.username}, "
            f"own_film_collection : {self.own_film_collection}, "
            f"follow_list : {self.follow_list}")

    def to_dict(self):
        """Hide password"""
        return {
            "id_user": self.id_user,
            "username": self.username,
            "own_film_collection": self.own_film_collection,
            "follow_list": self.follow_list,
        }

    class Config:
        # Options de configuration supplémentaires si nécessaire
        pass
