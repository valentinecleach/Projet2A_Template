# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse

import requests
from dotenv import load_dotenv

from src.Model.MovieMaker import MovieMaker


class MovieMakerTMDB:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3/"

    def get_movie_maker_by_id(self, tmdb_id: int) -> MovieMaker | None:
        # Reamarque : insomnia does not return the known_for with this request.
        """
                Retrieves details of a MovieMaker from TMDB by his TMDB ID.

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
            url = f"{self.base_url}/person{tmdb_id}?api_key={self.api_key}&language=en-US"
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
                    known_for="not specified with this request "
                )
            else:
                print(f"No MovieMaker found with TMDB ID : {tmdb_id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None

    def get_movie_maker_by_name(self, name: str) -> MovieMaker | None:
        # Reamarque : insomnia does not return the known_for with this request.
        """
                Retrieves details of a MovieMaker from TMDB by his name.

                Parameters:
                -----------
                name : str
                    The name of the MovieMaker on TMDB.

                Returns:
                --------
                MovieMaker | None
                    A MovieMaker object if found, otherwise None.
        """
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"{self.base_url}search/person?api_key={self.api_key}&language=en-US&query={encoded_name}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            # Si des résultats sont trouvés
            if 'results' in data and len(data['results']) > 0:
                first = data['results'][0]  # Prendre le premier résultat, sinon ajuster selon besoin
                return MovieMaker(
                    id_movie_maker=first['id'],
                    adult=first.get('adult', False),
                    name=first['name'],
                    gender=first.get('gender'),
                    biography=first.get('biography', ''),
                    birthday=first.get('birthday'),
                    place_of_birth=first.get('place_of_birth', ''),
                    deathday=first.get('deathday'),
                    known_for_department=first.get('known_for_department', ''),
                    popularity=first.get('popularity', 0.0),
                    known_for=first.get('known_for', [])
                )
            else:
                print(f"No MovieMaker found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None


# Test with TMDB ID 2710 (James Cameron) works !
# test with name "James Cameron" still doesn't work because all the parameters are not given by the request
# idea: allow to find by name, then find also by id, concatenate results to have a global MovieMaker.
if __name__ == "__main__":
    movie_maker_tmdb = MovieMakerTMDB()
    movie_maker = movie_maker_tmdb.get_movie_maker_by_name("James Cameron")
    if movie_maker:
        print("MovieMaker found:", movie_maker)
    else:
        print("MovieMaker not found.")
