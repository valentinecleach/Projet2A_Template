from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Comment:
    """Comment

    The comment of a movie. A user can comment a movie.

    """

    def __init__(
        self,
        user: ConnectedUser,
        movie: Movie,
        date: str,
        comment: str,
    ):
        self.user = user
        self.movie = movie
        self.date = date
        self.comment = comment

    def __str__(self):
        s = f"{self.user.username} commented"
        s+ = f"{self.comment} on the movie {self.movie.title}"
        s+ = f" on {self.date}"
        return s
