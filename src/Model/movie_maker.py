# Projet2A_Template\src\Model\MovieMaker.py
import re
from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from src.Model.movie import Movie

# mettre en anglais


class MovieMaker(BaseModel):   
    """
    Initializes a new MovieMaker object with the provided information. 
    A MovieMaker is a person in the film industry such as actors, directors etc.

    Parameters:
    -----------
    id_movie_maker : int
        A unique TMDB identifier for the person.
    adult : bool
        Indicates if the person is involved in adult content.
    name : str
        Name of the person.
    gender : int
        Indicates the gender of the person (1: female, 2: male, 3: non-binary).
    biography : str
        Biography of the person.
    birthday : str
        Birthdate (format YYYY-MM-DD).
    place_of_birth : str
        Place of birth.
    deathday : Optional[str] = None
        Date of death (format YYYY-MM-DD) or None.
    known_for_department : str
        The person's main department (e.g., directing, acting).
    popularity : float
        Popularity score.
    known_for : List[Movie]
        Movie linked to the MovieMaker
    """
    id_movie_maker: int 
    adult: bool = False 
    name: str
    gender: int 
    biography: str 
    birthday: Optional[date]
    place_of_birth: Optional[str]
    known_for_department: str 
    popularity: float
    known_for: Optional[List[Optional[Movie]]] 
    deathday: Optional[date] = None

    def __str__(self):
        """
        Returns a formatted string representation of the MovieMaker object.
        """
        return (f"MovieMaker(ID: {self.id_movie_maker}, Name: {self.name}, "
                f"Adult Content: {self.adult}, Gender: {self.gender}, "
                f"Biography: {self.biography}, Birthday: {self.birthday}, "
                f"Deathday : {self.deathday}"
                f"Place of Birth: {self.place_of_birth}, "
                f"Known For Department: {self.known_for_department}, "
                f"Popularity: {self.popularity})"
                f"Known for : {self.known_for}")
