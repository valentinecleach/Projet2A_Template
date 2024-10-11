from src.Model.movie import Movie
from src.Service.UserService import UserService


class User:
    def __init__(self, ip_address: str):
        """Initialisation"""
        self.ip_address = ip_address  # Adresse IP de l'utilisateur

    def search_movie_by_name(self, movie_name: str) -> Movie:
        """Search a movie by name.
        
        Parameters
        ----------
        movie_name : str
            The movies name
        
        Returns
        --------
        movie : Movie
        """
        pass

    def search_person_by_name(self, person_name: str):
        """permet de chercher un people du cinema (acteur, realisateur)"""

    def search_user(self, user_name: str):
        """Permet de chercher le profil d'un autre utilisateur""" 

    def sign_up(self):
        """Permet de créer un compte"""

    def log_in(self, email: str, password: str):
        """Permet de se connecter"""
