from src.Model.user import User

# from src.Service.password_service import create_salt, hash_password
# circular import


class ConnectedUser(User):
    def __init__(
        self,
        id_user: int,
        username: str,
        hashed_password: str,
        date_of_birth: str,
        gender: int,
        first_name: str,
        last_name: str,
        email_address: str,
        token: str,
        phone_number: str = None,
    ):
        # For all Users
        super().__init__(
            ip_address=None
        )  # Pas d'adresse IP pour l'utilisateur connecté

        # Info on users
        self.id_user = id_user
        self.username = username
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.gender = gender  # 1, 2, 3
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        # self.salt = create_salt(self.username)
        # self.hashed_password = hash_password(password, self.salt)
        # 2 lines above create a circular import
        self.salt = salt
        self.hashed_password = hashed_password

        # Collections associated with the connected user
        self.own_film_collection = []  # Liste des films ajoutés par l'utilisateur
        self.follow_list = []  # Liste des utilisateurs suivis

    def __str__(self):
        return f"id : {self.id_user}, username : {self.username}"
