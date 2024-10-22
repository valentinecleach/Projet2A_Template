from src.Model.user import User


class ConnectedUser(User):
    def __init__(
        self,
        id : int,
        name: str,
        pseudo: str,
        email: str,
        hashed_password: str,
        date_of_birth: str,
        gender: int,
        phone_number: str = None,
    ):
        super().__init__(
            ip_address=None
        )  # Pas d'adresse IP pour l'utilisateur connecté
        self.id_user = id
        self.name = name
        self.pseudo = pseudo
        self.email = email
        self.hashed_password = hashed_password  # hacher ce mot de passe
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.gender = gender
        self.own_film_collection = []  # Liste des films ajoutés par l'utilisateur
        self.follow_list = []  # Liste des utilisateurs suivis

    def __str__(self):
        return f"id : {self.id}, pseudo : {self.pseudo}"
