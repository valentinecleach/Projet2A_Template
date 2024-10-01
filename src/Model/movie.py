from genre import Genre
from pydantic import BaseModel
from rating import Rating


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
    belongs_to_collection : dict
        If there is a series
    budget : float
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

    def __init(self,
               id_movie,
               title,
               belongs_to_collection,
               budget,
               genre,
               origine_country,
               original_language,
               original_title,
               overview,
               popularity,
               release_date,
               revenue,
               runtime,
               vote_average,
               vote_count,
               adult=False
               ):

        if (not isinstance(id_movie, int)) or id_movie < 0 :
           TypeError("The id needs to be a positive integer")
        self.id_movie = id_movie

        if not isinstance(title, str):
           TypeError("The title must be a string")
        self.title = title

        if not isinstance(belongs_to_collection, dict):
           TypeError("belongs_to_collection must be a dictionnary")
        self.belongs_to_collection = belongs_to_collection

        if (not isinstance(budget, float)) or budget < 0 :
            TypeError("The budget must be a float")
        self.budget = budget

        if not isinstance(genre, List):
            raise TypeError("list")
        for i in genre:
            if not isinstance(i, Genre):
                raise TypeError("genre element of list not ok")
        self.genre = genre

        self.origine_country = origine_country
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity

        if not self._is_valid_date(release_date):
            raise ValueError("The release_date must be in the format YYYY-MM-DD.")
        self.release_date = release_date

        self.revenue = revenue
        self.runtime = runtime
        self.vote_average = vote_average
        self.vote_count = vote_count

        if adult:
            raise ValueError("The film can't be an adult film.")
        self.adult = adult
