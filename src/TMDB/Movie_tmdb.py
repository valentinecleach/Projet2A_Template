# interagir avec tmdb

import os
import urllib.parse
from typing import Dict, List

import requests
from dotenv import load_dotenv

# Model
from src.Model.movie import Movie

# Service
from src.Service.genre_service import GenreService
from src.Service.movie_collection_service import MovieCollectionService


class MovieTMDB:
    def __init__(self):
        """Constructor"""
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def get_movie_by_id(self, id_movie: int) -> Movie | None:
        """
        Retrieves details of a Movie from TMDB by it's ID given by TMDB.

        Parameters:
        -----------
        id_movie : int
            The ID of the Movie on TMDB.

        Returns:
        --------
        Movie | None
            A Movie object if found, otherwise None.
        """
        try:
            url = f"{self.base_url}/movie/{id_movie}?api_key={self.api_key}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if "id" in data:  # Checks if the ID is in response
                my_movie = {
                    "id_movie": data["id"],
                    "title": data["title"],
                    "belongs_to_collection": MovieCollectionService.create_list_of_collection(
                        data["belongs_to_collection"]
                    ),
                    "budget": data["budget"],
                    "genres": GenreService.create_list_of_genre(data["genres"]),
                    "origin_country": data["origin_country"],
                    "original_language": data["original_language"],
                    "original_title": data["original_title"],
                    "overview": data["overview"] if data["overview"] != "" else None,
                    "popularity": data["popularity"],
                    "release_date": data["release_date"] if data["release_date"] != "" else None,
                    "revenue": data["revenue"],
                    "runtime": data["runtime"],
                    "vote_average": 0, # We overwrite 0 on the vote average as we only want votes from our users.
                    "vote_count": 0,
                    "adult": data["adult"],
                }
                print(f"Movie {data['title']} get from TMDB")
                return Movie(**my_movie)
            else:
                print(f"No Movie found from TMDB with the ID : {id_movie}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movie from TMDB: ", str(e))
            return None

    ## get_by_id works. Quick test at the end of the file.

    def get_movies_by_title(self, title: str) -> Movie | None:
        """Retrieves details of a Movie from TMDB by title.
        Need to call get_by_id because of insomnia API

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
            encoded_name = urllib.parse.quote(title)
            url = f"{self.base_url}/search/movie?api_key={self.api_key}&language=en-US&query={encoded_name}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                movies = []
                for result in data["results"]:
                    id_movie = result["id"]
                    movies.append(self.get_movie_by_id(id_movie))
                return movies
            else:
                print(f"No Movie found with name : {title}.")
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

    # Pas nécéssaire ici (+ jai pas sauvegardé)
    def filter_by_popularity(self) -> list:
        """Filters by popularity all movies of the TMDB database and returns

        Parameters
        ----------

        Returns
        --------
        topmovies : list(Movie)
            The top movies from page 1.
        """
        try:
            url = f"{self.base_url}/movie/popular?api_key={self.api_key}&language=en-US&page=1"
            # url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
            headers = {"accept": "application/json", "Authorization": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            topmovies = []
            for movie in data["results"]:
                topmovies.append(
                    Movie(
                        # add things
                        """
                        "adult",
                        "genre_ids",
                        "id",
                        "original_language",
                        "original_title",
                        "overview",
                        "popularity",
                        "release_date",
                        "title",
                        "video",
                        "vote_average",
                        "vote_count"
                        """
                    )
                )
            return topmovies
        except requests.exceptions.RequestException as e:
            print("Error while fetching the movies: ", str(e))
            return None


# data2 = MovieTMDB()
# #print(data2.get_movie_by_id(7317))
# print(data2.get_movies_by_title("charlie et la chocolaterie"))
