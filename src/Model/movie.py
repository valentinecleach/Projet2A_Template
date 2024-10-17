from pydantic import BaseModel
from typing import List, Dict
# Model
from src.Model.genre import Genre
from src.Model.movie_collection import MovieCollection
# Service
from src.Service.static import _is_valid_date

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
               genres : List[Genre],
               origin_country : List[str],
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
        if not isinstance(belongs_to_collection, list):
            raise TypeError("belongs_to_collection must be a list of MovieCollection")        
        if (not isinstance(budget, float)) or budget < 0:
            raise TypeError("The budget must be a float")        
        if not isinstance(genres, list):
            raise TypeError("genre must be a Genre object.")
        for i in genres:
            if not isinstance(i, Genre):
                raise ValueError("genre element of list not ok")        
        if not isinstance(origin_country, List):
            raise TypeError("The origine country must be a list")        
        for data in origin_country:
            if not isinstance(data,str):
                raise ValueError("Each origin country must be a string")
        if not isinstance(original_language, str):
            raise TypeError("The original language must be a string")        
        if not isinstance(original_title, str):
            raise TypeError("The original title must be a string")              
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
        self.genres = genres
        self.origin_country = origin_country
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


# rapid test of the class

my_movie = {'id_movie': 1995, 
'title': 'Lara Croft: Tomb Raider', 
'belongs_to_collection': [ 'Movie Collection : Tomb Raider Collection'], 
'budget': 115000000, 
'genres': ['Genre : Adventure', 'Genre : Fantasy', 'Genre : Action', 'Genre : Thriller'], 
'origin_country': ['US'], 
'original_language': 'en', 
'original_title': 'Lara Croft: Tomb Raider', 
'overview': "Orphaned heiress, English aristocrat and intrepid archaeologist, Lara Croft, embarks on a dangerous quest to retrieve the two halves of an ancient artifact which controls time before it falls into the wrong hands. As an extremely rare planetary alignment is about to occur for the first time in 5,000 years, the fearless tomb raider will have to team up with rival adventurers and sworn enemies to collect the pieces, while time is running out. But, in the end, who can harness the archaic talisman's unlimited power?", 
'popularity': 39.097, 
'release_date': '2001-06-11', 
'revenue': 274700000, 
'runtime': 100, 
'vote_average': 5.9, 
'vote_count': 6009, 
'adult': False}

print(Movie(my_movie))
