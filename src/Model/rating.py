from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Rating:
    """Rating

    The rating of a movie. A user can rate a movie.
    """

    def __init__(
        self,
        user: ConnectedUser,
        movie: Movie,
        date: str,
        rating: int,
    ):
        self.user = user
        self.movie = movie
        self.date = date
        self.rating = rating

    def __str__(self):
        s = f"{self.user.username} give"
        s += f"{self.rating} over 10 to the movie {self.movie.title}"
        s += f" on {self.date}"
        return s
