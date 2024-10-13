# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse
import requests
from dotenv import load_dotenv
from src.Model.movie_maker import MovieMaker


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

    def get_movie_maker_by_name(self, name: str) -> list[MovieMaker] | None:
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
                results = data['results'] 
                movie_maker_results = []
                for result in results :
                    movie_maker_result.append(MovieMaker(
                        id_movie_maker = result['id'],
                        adult = result.get('adult', False),
                        name = result['name'],
                        gender = result.get('gender'),
                        biography = result.get('biography', ''),
                        birthday = result.get('birthday'),
                        place_of_birth = result.get('place_of_birth', ''),
                        deathday = result.get('deathday'),
                        known_for_department = result.get('known_for_department', ''),
                        popularity = result.get('popularity', 0.0),
                        known_for = result.get('known_for', [])
                        )
                    )
                return movie_maker_results
            else:
                print(f"No MovieMaker found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None


