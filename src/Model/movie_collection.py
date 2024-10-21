from datetime import datetime
from typing import List  # , Optional

from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class MovieCollection:
    """
    Class representing the collection of the movie.

    Parameters
    ----------
    id : int
        The id of the collection
    name : str
        The name of the collection

    Examples
    --------


    """

    def __init__(
        self, name: str, user: ConnectedUser, date: str, movie_list: List[Movie] = []
    ):
        """Constructor

        Parameters:
        -----------
        MovieCollection_data : dict
            A dictionary containing the collection of the movie data (id_user and id_Movie).
        """
        self.name = name
        self.movie_list = movie_list
        self.user = user
        self.date = date

    def __repr__(self):
        return f" 'Movie Collection : {self.name}' "


# Unrelated code to show sys.path to understand error with classes ipmports.
