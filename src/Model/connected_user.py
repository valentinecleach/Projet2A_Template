from pydantic import BaseModel
from src.Model.user import User
from datetime import date

class ConnectedUser(User):
    id_user: int
    username: str
    hashed_password: str
    date_of_birth: date
    gender: int  
    first_name: str
    last_name: str
    email_address: str
    password_token: str
    phone_number: str | None = None  # Optionnel

    # Collections associées à l'utilisateur connecté
    own_film_collection : list | None = None
    follow_list: list | None = None

    def __str__(self):
        return f"id: {self.id_user}, username: {self.username}"

    def to_dict(self):
        # Masque le mot de passe
        return {
            'username': self.username,
            'own_film_collection' : self.own_film_collection,
            'follow_list' : self.follow_list
        }

    class Config:
        # Options de configuration supplémentaires si nécessaire
        pass

