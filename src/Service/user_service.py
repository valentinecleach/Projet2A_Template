import bcrypt  # Assurez-vous d'avoir bcrypt installé pour le hachage
import psycopg2  # Assurez-vous d'avoir psycopg2 installé pour la connexion à PostgreSQL
from datetime import date

# DAO
from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.DAO.user_favorites import UserFavoritesDAO
from src.DAO.user_follow import UserFollowDAO


# Model
from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie
from src.Model.user import User

# Service
from src.Service.password_service import (
    check_password_strenght,
    create_salt,
    hash_password,
)

class UserService:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection  
        self.user_dao = UserDao(db_connection)

    def check_valid_username(self, username):
        if len(username) <= 5:
            raise ValueError("Username must contain at least 5 characters")
        existing_user = self.user_dao.get_user_by_name(username)
        print(existing_user)
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
        gender : int,
        date_of_birth : date,
        email_address: str,
        phone_number: str | None = None  # Optionnel
    ):
        """Permet de créer un compte utilisateur."""
        self.check_valid_username(username)
        check_password_strenght(password)

        salt = create_salt(username)
        hashed_password = hash_password(password, create_salt(username))

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
            "gender": gender
        }
        try:
            # Utilisation de la méthode insert de DBConnection
            self.user_dao.insert(user)
            print(f"Utilisateur '{username}' inscrit avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'inscription : {str(e)}")

##### sign_up fonctionne

    def log_in(self, username: str, password: str):
        """Permet à un utilisateur de se connecter."""

        # Hashage du mdp
        salted_password = create_salt(username)
        hashed_password = hash_password(password, salted_password)

        try:
            with self.db_connection.connection.cursor() as cursor:
                # Récupération de l'utilisateur de la base de données
                cursor.execute(
                    "SELECT hashed_password FROM users WHERE username = %s", (username,)
                )
                result = cursor.fetchone()

                if result and bcrypt.checkpw(
                    salted_password, result[0].encode("utf-8")
                ):
                    print(f"Utilisateur '{username}' connecté avec succès.")
                    # Retourner une instance de ConnectedUser avec les informations pertinentes
                    return ConnectedUser(
                        username=username, ip_address="placeholder_ip"
                    ) 
                else:
                    print(
                        "Échec de la connexion : nom d'utilisateur ou mot de passe incorrect."
                    )
                    return User(
                        ip_address="placeholder_ip"
                    )  # Retourne un User non connecté
        except Exception as e:
            print(f"Erreur lors de la connexion : {str(e)}")
            return User(ip_address="placeholder_ip")  # Retourne un User non connecté

    def search_user(self, username: str):
        """Permet de chercher le profil d'un autre utilisateur."""
        if not username:
            print("Le nom d'utilisateur est requis.")
            return None

        # Appel à la méthode get_user_by_name de UserDao
        users = self.user_dao.get_user_by_name(username)

        if users:
            return users  # Retourne une liste d'instances ConnectedUser correspondant à la recherche

        print("Aucun utilisateur trouvé pour le nom :", username)
        return None

    def follow(self, utilisateur):
        """Ajoute un utilisateur à la liste des éclaireurs."""

    def unfollow(self, utilisateur):
        """Supprime un utilisateur de la liste des éclaireurs."""

    def rate_film(self, film, rating: int):
        """Attribue une note à un film."""

    def add_comment(self, film, comment: str):
        """Ajoute un commentaire à un film."""

    def log_out(self):
        """Déconnexion de l'utilisateur."""

    def delete_account(self):
        """Suppression du compte de l'utilisateur."""


# db_connection = DBConnector()
# my_object = UserService(db_connection)
# user = {
#     'first_name': 'John',
#     'last_name': 'Doe',
#     'username': 'johndoe',
#     'password': 'SecurePassword123!',
#     'gender': 1,  # Exemple de genre (1 pour masculin, 2 pour féminin, selon votre définition)
#     'date_of_birth': date(1990, 12, 25), 
#     'email_address': 'john.doe@example.com',
#     'phone_number': '123-456-7890' 
# }
# my_object.sign_up(**user)
