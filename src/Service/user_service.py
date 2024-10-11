import bcrypt  # Assurez-vous d'avoir bcrypt installé pour le hachage
import psycopg2  # Assurez-vous d'avoir psycopg2 installé pour la connexion à PostgreSQL
from src.DAO.db_connection import DBConnection

class UserService:
    def __init__(self, db_connection : DBConnection):
        self.db_connection = db_connection  # Connexion à la base de données

    def sign_up(self, first_name: str, last_name: str, username: str, password: str, email_address: str):
        """Permet de créer un compte utilisateur."""
        
        # Validation de la longueur du nom d'utilisateur
        if len(username) < 5:
            raise ValueError("Le nom d'utilisateur doit comporter au moins 5 caractères.")

        # Création des parties de sel
        start_user = username[:3]  # Les trois premiers caractères du nom d'utilisateur
        end_user = username[3:]  # Les caractères restants du nom d'utilisateur

        # Hachage du mot de passe avec le sel
        salted_password = f"{start_user}{password}{end_user}".encode('utf-8')
        hashed_password = bcrypt.hashpw(salted_password, bcrypt.gensalt())

        # Préparation des valeurs à insérer
        values = (first_name, last_name, username, hashed_password, email_address)

        try:
            # Utilisation de la méthode insert de DBConnection
            self.db_connection.insert('users', values)
            print(f"Utilisateur '{username}' inscrit avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'inscription : {str(e)}")

    def log_in(self, username: str, password: str):
        """Permet à un utilisateur de se connecter."""
        
        # Validation de la longueur du nom d'utilisateur
        if len(username) < 5:
            raise ValueError("Le nom d'utilisateur doit comporter au moins 5 caractères.")
        
        # Création des parties de sel
        start_user = username[:3]  # Les trois premiers caractères du nom d'utilisateur
        end_user = username[3:]  # Les caractères restants du nom d'utilisateur
        
        # Hachage du mot de passe avec le sel
        salted_password = f"{start_user}{password}{end_user}".encode('utf-8')
        
        try:
            with self.db_connection.connection.cursor() as cursor:
                # Récupération de l'utilisateur de la base de données
                cursor.execute("SELECT hashed_password FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                
                if result and bcrypt.checkpw(salted_password, result[0].encode('utf-8')):
                    print(f"Utilisateur '{username}' connecté avec succès.")
                    # Retourner une instance de ConnectedUser avec les informations pertinentes
                    return ConnectedUser(username=username, ip_address="placeholder_ip")  # Remplacez par l'adresse IP réelle
                else:
                    print("Échec de la connexion : nom d'utilisateur ou mot de passe incorrect.")
                    return User(ip_address="placeholder_ip")  # Retourne un User non connecté
        except Exception as e:
            print(f"Erreur lors de la connexion : {str(e)}")
            return User(ip_address="placeholder_ip")  # Retourne un User non connecté

    def search_user(self, username: str):
        """Permet de chercher le profil d'un autre utilisateur."""

    def dao_function():
        """ parameters and methods to use DAO/db_connection; """

