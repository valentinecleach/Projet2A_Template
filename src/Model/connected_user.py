from src.Model.user import User

from src.Service.password_service import hash_password, create_salt


class ConnectedUser(User):
    def __init__(
        self,
        id_user : int,
        username: str,
        email: str,
        hashed_password: str,
        date_of_birth: str,
        gender: int, 
        phone_number: str = None,
        first_name: str,
        last_name: str,
        email_address: str
    ):
        super().__init__(
            ip_address=None
        )  # Pas d'adresse IP pour l'utilisateur connecté
        self.id_user = id_user
        self.username = username
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.gender = gender # 1, 2, 3
        self.own_film_collection = []  # Liste des films ajoutés par l'utilisateur
        self.follow_list = []  # Liste des utilisateurs suivis
        self.email_adress = email_adress
        self.first_name = first_name
        self.last_name = last_name
        self.salt = create_salt(self.username)
        self.hashed_password = hash_password(password, self.salt)  
        

    def __str__(self):
        return f"id : {self.id}, pseudo : {self.pseudo}"
