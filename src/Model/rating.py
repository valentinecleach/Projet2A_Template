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
        date: str,
        rating: int,
    ):
        self.user = ConnectedUser
        self.movie = movie
        self.date = date
        self.rating = rating

    def nb_ratings(self) -> int:
        """
        The number of users who have rated the movie

        Returns
        -------
        int
        """
        return len(self.who_rated)

    def update_rating(self, user: User, new_rating: Rating):
        if User in self.who_rated:
            raise ValueError("You cannot rate the movie twice")
        # pb one cannot change their rating
