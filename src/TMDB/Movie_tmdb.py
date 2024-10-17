# interagir avec tmdb

# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse

import requests
from dotenv import load_dotenv

from src.Model.genre import Genre
from src.Model.movie import Movie
from src.Model.movie_maker import MovieMaker
from src.Service.collection_service import CollectionService
from src.Service.genre_service import GenreService


class MovieTMDB:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def get_movie_by_id(self, id: int) -> Movie | None:
        """
        Retrieves details of a Movie from TMDB by his ID given by TMDB.

        Parameters:
        -----------
        id : int
            The ID of the Movie on TMDB.

        Returns:
        --------
        Movie | None
            A Movie object if found, otherwise None.
        """
        try:
            url = f"{self.base_url}/movie/{id}?api_key={self.api_key}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if "id" in data:  # check if id is in response
                return Movie(
                    id=data["id"],
                    title=data["title"],
                    belongs_to_collection=function_service_collection(
                        data["belongs to collection"]
                    ),
                    budget=data["budget"],
                    genre=function_service_genre(data["genre"]),
                    orginal_country=data["origine country"],
                    original_language=data["original language"],
                    original_title=data["original_title"],
                    overview=data["overview"],
                    popularity=data["popularity"],
                    release_date=data["release_date"],
                    revenu=data["revenu"],
                    vote_average=data["vote_average"],
                    vote_count=data["vote_count"],
                    adult=data["adult"],
                )
            else:
                print(f"No Movie found with the ID : {id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movie from TMDB: ", str(e))
            return None

    ######### suposed to be correct above

    def get_movie_by_name(self, name: str) -> Movie | None:
        """Retrieves details of a Movie from TMDB by his name.

        Parameters:
        -----------
        name : str
            The name of the Movie on TMDB.

        Returns:
        --------
        Movie | None
            A Movie object if found, otherwise None.
        """
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"{self.base_url}search/person?api_key={self.api_key}&language=en-US&query={encoded_name}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            # Si des résultats sont trouvés
            if "results" in data and len(data["results"]) > 0:
                first = data["results"][
                    0
                ]  # Prendre le premier résultat, sinon ajuster selon besoin
                return Movie(
                    id_movie=first["id"],
                    adult=first.get("adult", False),
                    title=first.get("title"),
                    # belongs_to_collection, budget, country
                    original_language=first.get("original_language"),
                    original_title=first.get("original_title"),
                    overview=first.get("overview"),
                    popularity=first.get("popularity"),
                    release_date=first.get("release_date"),
                    # revenue=first.get('overview'),
                    # runtime=first.get('overview'),
                    vote_average=first.get("vote_average"),
                    vote_count=first.get("vote_count"),
                )
            else:
                print(f"No Movie found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movie from TMDB: ", str(e))
            return None

    def view_comments(self, movie: str):
        """Shows the comments of a Movie

        Parameters
        ----------
        movie : str
            The movies name
        """
        pass

    def filter_by_genre(self, genre: int):
        """Filters a search by the genres id

        Parameters
        ----------
        genre : int
            The genre's id
        """
        pass

    def filter_by_popularity(self) -> Movie:
        """Filters by popularity

        Parameters
        ----------
        """
        pass

    def find_movie_maker(self, id_movie) -> MovieMaker:
        """Finds the movie makers of a movie

        Parameters
        ----------
        id_movie : str
            id of the movie

        Returns
        --------
        list(MovieMaker) | None
        """
        try:
            url = f"{self.base_url}/movie/{id_movie}/credits?api_key={self.api_key}&language=en-US"
            # "https://api.themoviedb.org/3/movie/21661/credits?language=en-US"
            headers = {"accept": "application/json", "Authorization": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            if "id_movie" == data["id"]:
                movie_makers = []
                for moviemakers in data["cast"]:
                    movie_makers.append(
                        MovieMaker(
                            id=moviemakers["id"],
                            adult=moviemakers["adult"],
                            name=moviemakers["name"],
                            gender=moviemakers["gender"],
                            biography=moviemakers["biography"],
                            birthday=moviemakers["birthday"],
                            place_of_birth=moviemakers["place_of_birth"],
                            known_for_department=moviemakers["known_for_department"],
                            popularity=moviemakers["popularity"],
                            deathday=moviemakers["deathday"],
                        )
                    )
            else:
                print(f"No movie makers found with the info given : {id_movie}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching the movie makers from TMDB: ", str(e))
            return None


# https://developer.themoviedb.org/reference/movie-credits
# get https://api.themoviedb.org/3/movie/{movie_id}/credits
"""
{
  "id": 21661,
  "cast": [
    {
      "adult": false,
      "gender": 2,
      "id": 7431,
      "known_for_department": "Acting",
      "name": "Kevin Zegers",
      "original_name": "Kevin Zegers",
      "popularity": 18.321,
      "profile_path": "/zRjasG4NXxKbe6e1c4enivAvfcH.jpg",
      "cast_id": 3,
      "character": "Josh Framm",
      "credit_id": "52fe4423c3a368484e0118c3",
      "order": 0
    },


    import requests

url = "https://api.themoviedb.org/3/movie/21661/credits?language=en-US"


response = requests.get(url, headers=headers)

print(response.text)
"""
