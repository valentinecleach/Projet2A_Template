from datetime import date

from pydantic import BaseModel, Field

# Model
from src.Model.genre import Genre
from src.Model.movie_collection import MovieCollection


class Movie(BaseModel):
    """Movie

    A series of moving pictures, usually shown in a cinema or on television and
    often telling a story

    Attributes
    ----------
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

    id_movie: int = Field(
        ..., gt=0, description="The id needs to be a positive integer"
    )
    title: str
    belongs_to_collection: Optional[List[MovieCollection]] = (
        None  # peut ne pas avoir de MovieCollection.
    )
    budget: Optional[int]
    genres: List[Genre]
    origin_country: Optional[List[str]]
    original_language: Optional[str]
    original_title: Optional[str]
    overview: Optional[str]
    popularity: Optional[float]
    release_date: Optional[date]  # pydantic convertit automatiuqement str en date.
    revenue: Optional[int]
    runtime: Optional[int]
    vote_average: Optional[float]
    vote_count: Optional[int]
    adult: bool = False

    def __str__(self):
        """
        Print a string representation of the Movie object.
        """
        return (
            f"Title : {self.title}, ( ID: {self.id_movie} ), "
            f"Release Date: {self.release_date}, Popularity: {self.popularity}, "
            f"Vote Average: {self.vote_average}, Vote Count: {self.vote_count}"
        )

    def __eq__(self, other):
        """compare two instances of the Movie class,checking
        whether their internal attributes are identical

        Attributes
        ----------
        other: any
            The object with which  "self" is compared
        """
        if isinstance(other, Movie):
            return self.__dict__ == other.__dict__
        return False

    # def __get_pydantic_core_schema__# ?,
