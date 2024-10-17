# interagir avec tmdb

# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse

import requests
from dotenv import load_dotenv
# Model
from src.Model.genre import Genre
from src.Model.movie import Movie
# Service
from src.Service.genre_service import GenreService
from src.Service.movie_collection_service import MovieCollectionService
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
            if 'id' in data:  # check if id is in response
                my_movie = {
                    'id_movie': data['id'],
                    'title': data['title'],
                    'belongs_to_collection': MovieCollectionService.create_list_of_collection(data['belongs_to_collection']),
                    'budget': data['budget'],
                    'genres': GenreService.create_list_of_genre(data['genres']),
                    'origin_country': data['origin_country'],
                    'original_language': data['original_language'],
                    'original_title': data['original_title'],
                    'overview': data['overview'],
                    'popularity': data['popularity'],
                    'release_date': data['release_date'],
                    'revenue': data['revenue'],
                    'runtime': data['runtime'],
                    'vote_average': data['vote_average'],
                    'vote_count': data['vote_count'],
                    'adult': data['adult']
                    }
                return my_movie                     
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

    def filter_by_popularity(self) -> list(Movie):
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

    def find_movie_maker(self, id_movie) -> MovieMaker:
        """Finds the movie makers of a movie

        Parameters
        ----------
        id_movie : str
            id of the movie

        Returns
        --------
        movie_makers : list(MovieMaker) | None
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

                return movie_makers
            else:
                print(f"No movie makers found with the info given : {id_movie}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching the movie makers from TMDB: ", str(e))
            return None


# https://developer.themoviedb.org/reference/movie-credits
# get https://api.themoviedb.org/3/movie/{movie_id}/credits
<<<<<<< HEAD
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

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjBlNWRlZDNkNzliYzVlNTcxNTM4MDMwZjdlNWFmOCIsIm5iZiI6MTcyODU4OTQ3OC4zODc3NDUsInN1YiI6IjY2ZTBhYmMyOWM3MzUzMmRkYmFhYWY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3XrjUtK_SJmltQGboTpJVLjwTgJ5fdIXtltmVMLX1bQ"
}

response = requests.get(url, headers=headers)

print(response.text)
"""
data2 = MovieTMDB()
print(data2.get_movie_by_id(1995))

=======
>>>>>>> f03a8cbaf15a63d5e4a64da61101593e81a1c783
