from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Comment:
    """Comment is an object that describes a users opinion on a movie.

    Attributes
    ----------
    user : ConnectedUser
        The user who wrote the comment
    movie : Movie
        The film with the commentary
    comment : str
        The comment that was posted
    date : str
        The date the comment was posted
    """

    def __init__(
        self,
        user: ConnectedUser,
        movie: Movie,
        comment: str,
        date: str
    ):
        """Constructor"""
        self.user = user
        self.movie = movie
        self.comment = comment
        self.date = date
        

    def __str__(self):
        """ shows the comment and corresponding information
        """ 
        s = f"<{self.user.username}> commented :"
        s = s + f" <{self.comment}> on the movie <{self.movie.title}>"
        s = s + f" on <{self.date}>"
        return s
