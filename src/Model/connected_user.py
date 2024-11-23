from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.Model.user import User


class ConnectedUser(User):
    """A ConnectedUser is a user that has an account in the app. This allows them to use certain features.

    Attributes
    ----------
    id_user : int
        The ID of the user
    username : str
        The pseudonym of the user
    hashed_password : str
        The password the user has created after been hashed
    date_of_birth : date
        The date of birth entered by the user
    gender : int
        The gender entered by the user
    first_name : str
        The first name of the user
    last_name : str
        The last name of the user
    email_adress : str
        The email adress of the user
    password_token : str
        An object used for password
    phone_number : str
        The phone number of user
    own_film_collection : list
        A list of ID's of favorite movies
    follow_list : list
        A list of ID's of users followed
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
        """user information: id and pseudonym"""
        return (
            f"id_user : {self.id_user}, "
            f"username : {self.username}, "
            f"own_film_collection : {self.own_film_collection}, "
            f"follow_list : {self.follow_list}"
        )

    def __repr__(self):
        """user information: id, pseudonym and saved lists: movie collection and subscriptions"""
        return (
            f"id_user : {self.id_user}, "
            f"username : {self.username}, "
            f"own_film_collection : {self.own_film_collection}, "
            f"follow_list : {self.follow_list}"
        )

    def to_dict(self):
        """Displays only a few information on an user"""
        return {
            "id_user": self.id_user,
            "username": self.username,
            "own_film_collection": self.own_film_collection,
            "follow_list": self.follow_list,
        }

    def to_dict_get_own(self):
        """Displays more information if a user wants to consult his own profile"""
        return {
            "id_user": self.id_user,
            "username": self.username,
            "date_of_birth": self.date_of_birth,
            "gender": self.first_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "own_film_collection": self.own_film_collection,
            "follow_list": self.follow_list,
        }
