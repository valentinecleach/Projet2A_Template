# src/TMDB/MovieMaker_tmdb.py
import os
import requests
from dotenv import load_dotenv
from src.Model.MovieMaker import MovieMaker
# Problème pour le known_for. Erreur dans le lien avec Movie 

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
                known_for_movies = []
                if 'known_for' in data:
                    for movie_data in data['known_for']:
                        # Assuming Movie has an appropriate constructor
                        movie = Movie(
                                id_movie=movie_data['id'],
                                title=movie_data['title'],
                                belongs_to_collection=movie_data.get('belongs_to_collection', {}),
                                budget=float(movie_data.get('budget', 0.0)),  # Assuming budget is a float
                                genre=[Genre(**g) for g in movie_data.get('genre', [])],  # Assuming Genre is defined elsewhere
                                origine_country=movie_data.get('origine_country', ''),
                                original_language=movie_data.get('original_language', ''),
                                original_title=movie_data.get('original_title', ''),
                                overview=movie_data.get('overview', ''),
                                popularity=float(movie_data.get('popularity', 0.0)),  # Assuming popularity is a float
                                release_date=movie_data.get('release_date', ''),
                                revenue=float(movie_data.get('revenue', 0.0)),  # Assuming revenue is a float
                                runtime=int(movie_data.get('runtime', 0)),  # Assuming runtime is an int
                                vote_average=float(movie_data.get('vote_average', 0.0)),  # Assuming vote_average is a float
                                vote_count=int(movie_data.get('vote_count', 0)),  # Assuming vote_count is an int
                                adult=movie_data.get('adult', False)  # Assuming adult is a boolean
                            )
                        known_for_movies.append(movie.__str__())

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
                    known_for=known_for_movies
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
