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
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection
        self.user_dao = UserDao(db_connection)

    def check_valid_username(self, username):
        if len(username) < 5:
            raise ValueError("Username must contain at least 5 characters")
        existing_user = self.user_dao.get_user_by_name(username, verif=True)
        if existing_user is not None:
            raise ValueError("This username is already taken.")
        else:
            print("good username")

    def check_valid_email_address(self, email):
        existing_user = self.user_dao.check_email_address(email)
        if existing_user is None:
            raise ValueError("This email address is already taken.")
        else:
            print("good email_address")

    def sign_up(
        self,
        first_name: str,
        last_name: str,
        username: str,
        password: str,
        gender: int,
        date_of_birth: date,
        email_address: str,
        phone_number: str | None = None,  # Optionnel
    ) -> ConnectedUser:
        """Permet de créer un compte utilisateur."""
        try:
            self.check_valid_username(username)
            self.check_valid_email_address(email_address)
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
            # Utilisation de la méthode insert de DBConnection
            connected_user = self.user_dao.insert(user)
            print(
                f"User '{connected_user.username}' successfully sign_up. His id is {connected_user.id_user}"
            )
            return connected_user
        except ValueError as e:
            raise ValueError(f"Error during user registration: {str(e)}")
            return None
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")
            return None

    ##### sign_up fonctionne

    def log_in(self, username: str, password_tried: str):
        """Permet à un utilisateur de se connecter."""
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
                    # Retourner une instance de ConnectedUser avec les informations pertinentes
                    return True
            else:
                print(
                    "Échec de la connexion : nom d'utilisateur ou mot de passe incorrect."
                )
        except Exception as e:
            print(f"Erreur : {str(e)}")
