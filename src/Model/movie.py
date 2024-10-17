from pydantic import BaseModel
from typing import List, Dict
# Model
from src.Model.genre import Genre
from src.Model.movie_collection import MovieCollection
# Service
from src.Service.static import _is_valid_date
from src.Service.movie_collection_service import MovieCollectionService
from src.Service.genre_service import GenreService
# from src.Model.Rating import Rating


class Movie():
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
               id_movie : int,
               title : str,
               belongs_to_collection : List[MovieCollection],
               budget,
               genre : List[Genre],
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

        if not isinstance(id_movie, int) or id_movie < 0:
            raise TypeError("The id needs to be a positive integer")        
        if not isinstance(title, str):
            raise TypeError("The title must be a string")        
        if not isinstance(belongs_to_collection, List[MovieCollection]):
            raise TypeError("belongs_to_collection must be a list of MovieCollection")        
        if (not isinstance(budget, float)) or budget < 0:
            raise TypeError("The budget must be a float")        
        if not isinstance(genre, Genre):
            raise TypeError("genre must be a Genre object.")
        for i in genre:
            if not isinstance(i, Genre):
                raise ValueError("genre element of list not ok")        
        if not isinstance(origine_country, str):
            raise TypeError("The origine country must be a string")        
        if not isinstance(original_language, str):
            raise TypeError("The original language must be a string")        
        if not isinstance(original_title, str):
            raise TypeError("The original title must be a string")        
        if not isinstance(origine_country, str):
            raise TypeError("The origine country must be a string")        
        if not isinstance(popularity, float):
            raise TypeError("The popularity must be a float")        
        if not _is_valid_date(release_date):
            raise ValueError("The release_date must be in the format YYYY-MM-DD.")
        if not isinstance(revenue, float):
            raise TypeError("The revenue must be a float")
        if not isinstance(runtime, ):
            raise TypeError("The runtime must be a ")
        if not isinstance(vote_average, ):
            raise TypeError("The vote_average must be a ")       
        if not isinstance(vote_count, int):
            raise TypeError("The vote count must be a integer")
        if not isinstance(adult, bool):
            raise TypeError("bool")
        if adult:
            raise ValueError("The film can't be an adult film.")

        self.id_movie = id_movie
        self.title = title
        self.belongs_to_collection = belongs_to_collection
        self.budget = budget
        self.genre = genre
        self.origine_country = origine_country
        self.original_language = original_language
        self.original_title = original_title
        self.overview = overview
        self.popularity = popularity
        self.release_date = release_date
        self.revenue = revenue
        self.runtime = runtime
        self.vote_average = vote_average
        self.vote_count = vote_count
        self.adult = adult

    def __str__(self):
            """
            Returns a string representation of the Movie object.
            """
            return (f"Title : {self.title}' : ID: {self.id_movie},"
                    f"Release Date: {self.release_date}, Popularity: {self.popularity}, "
                    f"Vote Average: {self.vote_average}, Vote Count: {self.vote_count})")


# to check the constructor with insomnia data :
