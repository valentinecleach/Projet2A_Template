from user import User


class Rating:
    """Rating

    The rating of a film. A user can rate a film ou of ?? stars if they liked
    it.

    Parameters
    ----------
    overall_rating : int
        The average rating

    who_rated : list[Users]
        The list of people who have rated the film

    Examples:
    --------

    """
    def __init__(self):
        self.overall_rating = 0
        self.who_rated = []

    def nb_ratings(self) -> int:
        """
        The number of users who have rated the film

        Returns
        -------
        int
        """
        return len(self.who_rated)

    def update_rating(self, user: User, new_rating: Rating):
        if User in self.who_rated:
            raise ValueError("You cannot rate the film twice")
        # pb one cannot change their rating
