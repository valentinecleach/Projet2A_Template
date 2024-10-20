from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Comment:
    """Comment

    The comment of a movie. A user can comment a movie
    it.

    Parameters
    ----------
    overall_comment : int
        The total number of comments
    Examples:
    --------

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
