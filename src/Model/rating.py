from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Rating:
    """Rating

    The rating of a movie. A user can rate a movie ou of ?? stars if they liked
    it.

    Parameters
    ----------
    overall_rating : int
        The average rating

    who_rated : list[Users]
        The list of people who have rated the movie
    Examples:
    --------

    """

    def __init__(
        self,
        user: ConnectedUser,
        movie: Movie,
        date: str,  # import datetime
        rating: int,
    ):
        self.user = user
        self.movie = movie
        self.date = date
        self.rating = rating

    def __str__(self):
        return f"{self.id}"

    def nb_ratings(self) -> int:
        """
        The number of users who have rated the movie

        Returns
        -------
        int
        """
        return len(self.who_rated)
