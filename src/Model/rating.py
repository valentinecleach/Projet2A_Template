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
        rate: int
    ):
        """Constructor"""
        self.user = user
        self.movie = movie
        self.date = date
        self.rate = rate

    def __str__(self):
        """Display method for a film collection."""
        s = f"<{self.user.username}> rated"
        s = s + f" <{self.rate}> over 10 to the movie <{self.movie.title}>"
        s = s + f"  on <{self.date}>"
        return s

    def __repr__(self):
        """Display method for a film collection."""
        return (f"Rating(user={self.user!r}, rate={self.rate!r}, "
                f"movie={self.movie!r}, date={self.date!r})")
