
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
        id_user: int,
        id_movie: int,
        date: str,  # import datetime
        rating: int,
    ):
        self.id_user = id_user
        self.id_movie = id_movie
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
