from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie
from datetime import date


class Rating:
    """Rating

    The rating of a movie. A user can rate a movie.
    """

    def __init__(
        self,
        user: ConnectedUser,
        movie: Movie,
        date: date,
        rate: int,
    ):
        self.user = user
        self.movie = movie
        self.date = date
        self.rate = rate

    def __str__(self):
        s = f"{self.user.username} rated"
        s = s + f" {self.rating} over 10 to the movie {self.movie.title}"
        s = s + f"  on {self.date}"
        return s
