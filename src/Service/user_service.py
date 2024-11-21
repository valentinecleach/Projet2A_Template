from datetime import date

# DAO
from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao

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
        phone_number: str | None = None,  # Optionnel
    ):
        """Permet de créer un compte utilisateur."""
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
            self.user_dao.insert(user)
            print(f"Utilisateur '{username}' inscrit avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'inscription : {str(e)}")

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


# db_connection = DBConnector()
# my_object = UserService(db_connection)
# # user = {
# #     'first_name': 'John',
# #     'last_name': 'Doe',
# #     'username': 'johndoe',
# #     'password': 'SecurePassword123!',
# #     'gender': 1,  # Exemple de genre (1 pour masculin, 2 pour féminin, selon votre définition)
# #     'date_of_birth': date(1990, 12, 25),
# #     'email_address': 'john.doe@example.com',
# #     'phone_number': '123-456-7890'
# # }
# # my_object.sign_up(**user)
# print(my_object.log_in("user1", "passworduser1"))
