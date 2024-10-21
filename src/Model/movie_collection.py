from datetime import datetime
from typing import List  # , Optional
from typing import Dict


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

    def __init__(self, movie_collection_data: Dict):
        """Constructor

        Parameters:
        -----------
        MovieCollection_data : dict
            A dictionary containing the collection of the movie data.
        """
        self.name = movie_collection_data.get("name")
        self.id = movie_collection_data.get("id")

    def __repr__(self):
        return f" 'Movie Collection : {self.name}' "


# Unrelated code to show sys.path to understand error with classes ipmports.
