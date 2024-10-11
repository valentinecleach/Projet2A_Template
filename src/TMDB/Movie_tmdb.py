# interagir avec tmdb

# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse

import requests
from dotenv import load_dotenv

from src.Model.genre import Genre
from src.Model.movie import Movie


class MovieTMDB:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")  
        self.base_url = "https://api.themoviedb.org/3/"

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
            url = f"{self.base_url}/person{id}?api_key={self.api_key}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if 'id' in data:  # check if id is in response
                return Movie(
                    id=data.get['id'],
                    adult=data.get('adult', False),
                    title=data.get["title"],
                    # budget=

                    # Plusieurs options pour le Genre. A voir lequel marche...
                    # Option 1:
                    genre=[Genre(id=data.get('genre_ids')[i]) for i in data.get('genre_ids')],
                    
                    # Option 2:
                    if len(data.get('genre_ids'))=1:
                        genre=Genre(id=data.get('genre_ids'), name = "")
                        else:
                            data_genre=data.get('genre_ids')
                            for i in data_genre:
                                genre = Genre(id = i, name = "")

                    # orginal_country= not filled out with insomnia
                    original_title=data.get['original_title'],
                    overview=data.get['overview'],
                    popularity=data.get['popularity'],
                    release_date=data.get['release_date'],
                    # revenue + runtime not avalible
                    vote_average=data.get['vote_average'],
                    vote_count=data.get['vote_count']
                )
            else:
                print(f"No Movie found with the ID : {id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movie from TMDB: ", str(e))
            return None

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
            if 'results' in data and len(data['results']) > 0:
                first = data['results'][0]  # Prendre le premier résultat, sinon ajuster selon besoin
                return Movie(
                    id_movie=first['id'],
                    adult=first.get('adult', False),
           
                )
            else:
                print(f"No Movie found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movier from TMDB: ", str(e))
            return None

