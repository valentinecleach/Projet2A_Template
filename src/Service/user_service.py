from datetime import date

# DAO
from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser

# Service
from src.Service.password_service import (
    check_password_strenght,
    create_salt,
    hash_password,
    verify_password,
)


class UserService:
    """ A User object in our service layer

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    user_dao : UserDao
        A DAO object used for operations related to users.
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)

    def check_valid_username(self, username):
        """ Checks if a username is valid. 
        It is valid if it has enough characters and doesn't already exist.
        
        Parameters
        ----------
        username : str
            The username to test
        """
        if len(username) < 5:
            raise ValueError("Username must contain at least 5 characters")
        existing_user = self.user_dao.get_user_by_name(username)
        if existing_user is not None:
            raise ValueError("This username is already taken.")
        else:
            print("good username")

    def sign_up(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        gender: int,
        date_of_birth: date,
        email_address: str,
        phone_number: str | None = None,  # Optional
    ) -> ConnectedUser:
        """Allow to create a user account.
        
        Parameters
        ----------
        first_name : str
            The user's first name.
        last_name : str
            The user's surname.
        username : str
            A username.
        password : str
            A password
        gender : int
            A number corresponding to a gender (1: man, 2: woman, 3: non-binary)
        date_of_birth : date
            A date of birth
        email_address : str
            An email address.
        phone_number : str , optional
            A phone number

        Returns
        -------
        ConnectedUser | None
            A connected user with the information given.
            If the user can't be created, thge method will return None.
        """
        try:
            self.check_valid_username(username)
            check_password_strenght(password)
            salt = create_salt(username)
            hashed_password = hash_password(password, salt)

            # Préparation des valeurs à insérer
            user = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "password_token": salt[-1],  # Dernière valeur de la liste `salt`
                "hashed_password": hashed_password,
                "email_address": email_address,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "gender": gender,
            }
            try:
                # Utilisation de la méthode insert de DBConnection
                connected_user = self.user_dao.insert(user)
                print(
                    f"User '{connected_user.username}' successfully sign_up. His id is {connected_user.id_user}"
                )
                return connected_user
            except Exception as e:
                print(f"Erreur lors de l'inscription : {str(e)}")
        except ValueError as e:
            print(f"Error during user registration: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


    def log_in(self, username: str, password_tried: str):
        """Allows a user to log in.
        
        Parameters
        ----------
        username : str
            The username
        password_tried : str
            A password to try and log in.
        """
        user = self.user_dao.get_user_by_name(username)
        user_password_token = user[0].password_token
        try:
            query = """
                SELECT hashed_password FROM users WHERE username = %s
            """
            value = (username,)
            result = self.db_connection.sql_query(query, value, return_type="one")
            hashed_password = result["hashed_password"]
            if hashed_password:
                verification = verify_password(
                    username, password_tried, user_password_token, hashed_password
                )
                if verification:
                    print(f"Utilisateur '{username}' connecté avec succès.")
                    # Returs an instance of ConnectedUser with the informations.
                    return True
            else:
                print(
                    "Échec de la connexion : nom d'utilisateur ou mot de passe incorrect."
                )
        except Exception as e:
            print(f"Erreur : {str(e)}")
