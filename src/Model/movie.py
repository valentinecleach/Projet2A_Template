from typing import Dict, List

from pydantic import BaseModel

# Model
from src.Model.Genre import Genre
from src.Model.movie_collection import MovieCollection

# Utils
from src.Utils.utils import _is_valid_date

# from src.Model.Rating import Rating


class Movie(BaseModel):
    """Movie

    A series of moving pictures, usually shown in a cinema or on television and
    often telling a story

    Parameters:
    -----------
    id_movie : int
        The id of a movie
    title : str
        The original title of a movie
    adult : bool
        If the movie is an adult movie, adult = True. Here we wil only have
        movies that aren't adult movies.
    belongs_to_collection : MovieCollection
        If there is a series
    budget : int
        The budget in $.
    genre : list[Genre]
        A movie can have one or multiple genres. They are kept in a list of
        Genre.
    origine_country : list[str]
        The movie can originate from one or multiple countries
    original_language : str
        The language
    original_title : str
        The original title
    overview : str
    popularity : float
        ?? (for the recommendation algorithm)
    release_date : str
        The release date. It's format is YYYY-MM-DD.
    revenue : int
        The revenue in $
    runtime : int
        The runtime (mins?)
    vote_average : float
        The current average float
    vote_count : int
        The amount of votes that the film has
    Examples
    --------

    """

    id_movie: int
    title: str
    # attention la ligne suivante ne marche pas car pydantic ne connait pas MovieCollection je crois
    belongs_to_collection: List[MovieCollection]
    budget: float
    genres: List[Genre]
    origin_country: List[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    release_date: str
    revenue: float
    runtime: str
    vote_average: float
    vote_count: int
    adult: bool = False

    def __str__(self):
        """
        Print a string representation of the Movie object.
        """
        return (
            f"Title : {self.title}', ID: {self.id_movie}, "
            f"Release Date: {self.release_date}, Popularity: {self.popularity}, "
            f"Vote Average: {self.vote_average}, Vote Count: {self.vote_count}"
        )

    # def __get_pydantic_core_schema__# ?,


# rapid test of the class
