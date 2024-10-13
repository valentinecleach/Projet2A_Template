# Projet2A_Template\src\Model\MovieMaker.py
import re
from datetime import datetime
from typing import Optional, List
from src.Model.movie import Movie
from src.Service.movie_maker_service import MovieMakerService as MMS

# mettre en anglais


class MovieMaker:
    def __init__(self, id_movie_maker: int, adult: bool, name: str,
                 gender: int, biography: str, birthday: str,
                 place_of_birth: str, deathday: Optional[str] = None, known_for_department: str,
                 popularity: float, known_for: List[Movie]):
        """
        Initializes a new MovieMaker object with the provided information.

        Parameters:
        -----------
        id_movie_maker : int
            Unique TMDB identifier for the person.
        adult : bool
            Indicates if the person is involved in adult content.
        name : str
            Name of the person.
        gender : int
            Indicates the gender of the person (2: male).
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
        """

        if not isinstance(id_movie_maker, int) or id_movie_maker < 0:  # 2710 for James Cameron
            raise ValueError("id_movie_maker must be a positive integer.")

        if adult is not False:
            raise ValueError("adult must be False.")

        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("name must be a non-empty string.")

        if not isinstance(biography, str):
            raise ValueError("biography must be a string.")

        # Validation of birthday (format YYYY-MM-DD)
        if not MMS._is_valid_date(birthday):
            raise ValueError("birthday must be in the format YYYY-MM-DD.")

        if not isinstance(place_of_birth, str):
            raise ValueError("place_of_birth must be a string.")

        # Validation of deathday (empty or in the format YYYY-MM-DD)
        if deathday and not MMS._is_valid_date(deathday):  # first part for living person
            raise ValueError("deathday must be empty or in the format YYYY-MM-DD.")

        if not isinstance(known_for_department, str):
            raise ValueError("known_for_department must be a string.")

        if not isinstance(popularity, float) or popularity < 0:
            raise ValueError("popularity must be a positive float.")

        if not isinstance(known_for, list):
            raise TypeError("known_for must be a list.")

        for movie in known_for:
            if not isinstance(movie, Movie):
                raise ValueError("known_for must be a list of Movie objects.")


        self.id_movie_maker = id_movie_maker
        self.adult = adult
        self.name = name
        self.gender = gender
        self.biography = biography
        self.birthday = birthday
        self.place_of_birth = place_of_birth
        self.deathday = deathday
        self.known_for_department = known_for_department
        self.popularity = popularity
        self.known_for = known_for

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
