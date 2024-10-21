from datetime import datetime
from typing import List, Dict


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
        self, movie_collection_data : Dict
    ):
        self.name = movie_collection_data.get('name')
        self.id = movie_collection_data.get('id')

    def __repr__(self):
        return f" 'Movie Collection : {self.name}' "


# Unrelated code to show sys.path to understand error with classes ipmports.
