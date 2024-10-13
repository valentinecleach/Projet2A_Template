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
            url = f"{self.base_url}/movie{id}?api_key={self.api_key}&language=en-US"
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
                    data_genres=data.get('genre_ids')
                    if len(data_genres) == 1:
                        genre=Genre(id=data_genres[0], name = "")
                    else:
                        genre=[]
                        for genre_id in data_genres:
                            genre.append(Genre(id = genre_id, name = ""))

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
                    title=first.get('title'),
                    #belongs_to_collection, budget, country
                    original_language=first.get('original_language')
                    original_title=first.get('original_title'),
                    overview=first.get('overview'),
                    popularity=first.get('popularity'),
                    release_date=first.get('release_date'),
                    # revenue=first.get('overview'),
                    # runtime=first.get('overview'),
                    vote_average=first.get('vote_average'),
                    vote_count=first.get('vote_count')
                )
            else:
                print(f"No Movie found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching Movie from TMDB: ", str(e))
            return None

    def view_comments(self, movie : str):
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
        """ Filters by popularity

        Parameters
        ----------
        """
        pass

    def find_movie_maker(self, movie : str) -> MovieMaker:
        """ Finds the movie makers of a movie
        
        Parameters
        ----------
        movie : str
            The movies name
        
        Returns
        -------
        moviemakers = list[MovieMaker] | None
        """
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"{self.base_url}search/person?api_key={self.api_key}&language=en-US&query={encoded_name}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            # Si des résultats sont trouvés
            if 'results' in data and len(data['results']) > 0:
                moviemakers=[]
                for moviemaker in  
                moviemakers.append(MovieMaker( 
                    id_movie_maker= ,
                    adult= ,
                    name= ,
                    gender= ,
                    biography= ,
                    birthday= ,
                    place_of_birth= ,
                    deathday= ,
                    known_for_departement= ,
                    popularity=
                 ))
                return moviemakers
            else:
                print(f"No Movie found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching the Movie Makers from TMDB: ", str(e))
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

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmYjBlNWRlZDNkNzliYzVlNTcxNTM4MDMwZjdlNWFmOCIsIm5iZiI6MTcyODU4OTQ3OC4zODc3NDUsInN1YiI6IjY2ZTBhYmMyOWM3MzUzMmRkYmFhYWY0NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3XrjUtK_SJmltQGboTpJVLjwTgJ5fdIXtltmVMLX1bQ"
}

response = requests.get(url, headers=headers)

print(response.text)
"""