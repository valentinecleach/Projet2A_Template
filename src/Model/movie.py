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
               adult = False,
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
               vote_count
               ):
        self.id_movie = id_movie
        self.title = title
        if adult:
            raise ValueError("The film can't be an adult film.")
        self.adult = adult
        self.belongs_to_collection  = belongs_to_collection
        self.budget = budget
        self.genre = genre
        self.origine_country= origine_country,
        self.original_language = original_language,
        self.original_title = original_title,
        self.overview = overview,
        self.popularity = popularity,
        if isinstance(release_date, str) is False:
            raise TypeError("Release date must be a string")
        if (release_date[4] != "-") or (release_date[] != "-"):
            raise ValueError("Wrong format for film")
        # ...YYYY-MM-DD
        self.release_date = release_date

        self.revenue = revenue,
        self.runtime = runtime,
        self.vote_average = vote_average,
        self.vote_count = vote_count

