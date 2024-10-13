# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse
import requests
from dotenv import load_dotenv
from src.Model.movie_maker import MovieMaker
from src.Service.movie_service import MovieService
from typing import List


class MovieMakerTMDB:
    def __init__(self):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.movie_service = MovieService(None)

    def get_movie_maker_by_id(self, tmdb_id: int) -> List | None:
        # Reamarque : insomnia does not return the known_for with this request.
        """
            Retrieve a MovieMaker by name or ID, combining the information from both sources if necessary.

            Parameters:
            -----------
            name : str | None
                The name of the MovieMaker.
            id_movie_maker : int | None
                The ID of the MovieMaker.

            Returns:
            --------
            List[MovieMaker] | None
                A list of MovieMaker objects or None if not found.
        """
        try:
            url = f"{self.base_url}/person/{tmdb_id}?api_key={self.api_key}&language=en-US"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()
            if 'id' in data:  # check if id is in response
                return [data['id'],
                        data['adult'],
                        data['name'],
                        data['gender'],
                        data['biography'],
                        data['birthday'],
                        data['place_of_birth'],
                        data['known_for_department'],
                        data['popularity'],
                        data['deathday']
                ]
            else:
                print(f"No MovieMaker found with TMDB ID : {tmdb_id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None

    def get_movie_maker_by_name(self, name: str) -> list[List] | None:
        # Reamarque : insomnia does not return thebiography, birthday, place of birth, deathday with this request.
        """
                Intermediate function that retrieves the information we are interested in for a movie maker on TMDB using its name. 

                Parameters:
                -----------
                name : str
                    The name of the MovieMaker on TMDB.

                Returns:
                --------
                List[List] | None
                    List of List with attributs 'id' and 'know for' for each moviemaker with the name of the request. 
        """
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"{self.base_url}/search/person?api_key={self.api_key}&language=en-US&query={encoded_name}"
            response = requests.get(url)
            response.raise_for_status()  # Raises an exception for HTTP error codes.
            data = response.json()

            # Si des résultats sont trouvés
            if 'results' in data and len(data['results']) > 0:
                results = data['results'] 
                movie_maker_results = []
                for result in results :
                    movie_maker_results.append([
                        result['id'],
                        self.movie_service.create_movies(result['known_for'])
                        ]
                    )
                return movie_maker_results
            else:
                print(f"No MovieMaker found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None

    def get_movie_maker_by_name_or_by_id(self, name: str | None = None, id_movie_maker: int | None = None) -> list[MovieMaker] | None:
        """
            function 

            Parameters :
            ---------------


            Returns :
            --------------

        """
        if name and id_movie_maker:
            raise ValueError("You cannot provide both 'name' and 'id_movie_maker'. Please provide only one.")

        movie_maker_results = []

        if name:
            results = self.get_movie_maker_by_name(name)
            if results:
                for data in results:
                    id_r = data[0]  # get the ID
                    result2 = self.get_movie_maker_by_id(id_r) 
                    if result2:
                        attributes = result2[:-1] + [data[1]] + result2[-1:]  # Concateante result2 with "known_for"
                        print(attributes)
                        movie_maker_results.append(MovieMaker(*attributes))  
            return movie_maker_results

        if id_movie_maker:
            result = self.get_movie_maker_by_id(id_movie_maker)
            if result:
                name_r = result[2]  # name is index 2
                result2 = self.get_movie_maker_by_name(name_r)
                if result2:
                    known_for = result2[0][-1]  
                    movie_maker_results.append(MovieMaker(*(result[:-1] + [known_for] + result[-1:]))) 
            return movie_maker_results
        return None

""""
# Ajouter ce bloc pour tester la recherche de "James Cameron"
if __name__ == "__main__":
    tmdb = MovieMakerTMDB()
    movie_makers = tmdb.get_movie_maker_by_name_or_by_id("James Cameron")
    if movie_makers:
        for maker in movie_makers:
            print(f"Found: {maker.name}, ID: {maker.id_movie_maker}")
    else:
        print("No movie makers found.")
"""