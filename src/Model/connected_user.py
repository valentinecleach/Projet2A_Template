from src.Model.user import User


class ConnectedUser(User):
    def __init__(
        self,
        name: str,
        pseudo: str,
        email: str,
        password: str,
        date_of_birth: str,
        gender: int,
        phone_number: str = None,
    ):
        super().__init__(
            ip_address=None
        )  # Pas d'adresse IP pour l'utilisateur connecté
        self.name = name
        self.pseudo = pseudo
        self.email = email
        self.password = password  # hacher ce mot de passe
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.gender = gender
        self.own_film_collection = []  # Liste des films ajoutés par l'utilisateur
        self.follow_list = []  # Liste des utilisateurs suivis

    def __str__(self):
        return f"id : {self.id}, pseudo : {self.pseudo}"

    def add_film(self, film: Movie):
        """Ajoute un film à la collection de l'utilisateur."""
        self.film_collection.append(film)

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
