# src/TMDB/MovieMaker_tmdb.py

import os

import requests
from dotenv import load_dotenv

from Model.MovieMaker import MovieMaker


class MovieMakerTMDB:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")  # Assurez-vous que la clé API est définie dans votre .env
        self.base_url = "https://api.themoviedb.org/3/person/"

    def get_movie_maker_by_id(self, tmdb_id: int) -> MovieMaker | None:
        """
                Retrieves details of a MovieMaker from TMDB by their TMDB ID.

                Parameters:
                -----------
                tmdb_id : int
                    The ID of the MovieMaker on TMDB.

                Returns:
                --------
                MovieMaker | None
                    A MovieMaker object if found, otherwise None.
        """
        try:
            url = f"{self.base_url}{tmdb_id}?api_key={self.api_key}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if 'id' in data:  # check if id is in response
                return MovieMaker(
                    id_movie_maker=data['id'],
                    adult=data.get('adult', False),
                    name=data['name'],
                    gender=data.get('gender'),
                    biography=data.get('biography', ''),
                    birthday=data.get('birthday'),
                    place_of_birth=data.get('place_of_birth', ''),
                    deathday=data.get('deathday'),
                    known_for_department=data.get('known_for_department', ''),
                    popularity=data.get('popularity', 0.0),
                )
            else:
                print(f"No MovieMaker found with TMDB ID : {tmdb_id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None


# Test with TMDB ID 2710 (James Cameron)
if __name__ == "__main__":
    movie_maker_tmdb = MovieMakerTMDB()
    movie_maker = movie_maker_tmdb.get_movie_maker_by_id(2710)
    if movie_maker:
        print("MovieMaker found:", movie_maker)
    else:
        print("MovieMaker not found.")
