from datetime import date

from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Rating:
    """Rating

    The rating of a movie. A user can rate a movie from zero to ten.

    Attributes
    ----------
    user : ConnectedUser
        The user who rated the movie
    movie : Movie
        The movie that was rated
    date : date
        The date of when the ratin,g was published
    rate : int
        The worth of a movie on a scale from zero to ten. 
    """

    def __init__(self, user: ConnectedUser, movie: Movie, date: date, rate: int):
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
        s = f"Rating(user={self.user!r}, rate={self.rate!r}, "
        s = s + f"movie={self.movie!r}, date={self.date!r})"
        return s
