from pydantic import BaseModel
from src.Model.user import User

class ConnectedUser(User):
    id_user: int
    username: str
    hashed_password: str
    date_of_birth: str
    gender: int  
    first_name: str
    last_name: str
    email_address: str
    password_token: str
    phone_number: str | None = None  # Optionnel

    # Collections associées à l'utilisateur connecté
    own_film_collection : list
    follow_list: list 

    def __str__(self):
        return f"id: {self.id_user}, username: {self.username}"

    class Config:
        # Options de configuration supplémentaires si nécessaire
        pass

