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
        comment: str,
        date: str
    ):
        self.user = user
        self.movie = movie
        self.comment = comment
        self.date = date
        

    def __str__(self):
        s = f"<{self.user.username}> commented :"
        s = s + f" <{self.comment}> on the movie <{self.movie.title}>"
        s = s + f" on {self.date}"
        return s
