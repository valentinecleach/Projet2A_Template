from src.Model.movie import Movie
from src.Service.user_service import UserService


class User:
    def __init__(self, ip_address: str):
        """Initialisation"""
        self.ip_address = ip_address  # Adresse IP de l'utilisateur

