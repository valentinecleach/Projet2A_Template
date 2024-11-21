# src/TMDB/MovieMaker_tmdb.py
import os
import urllib.parse
import requests
from dotenv import load_dotenv
from src.Model.movie_maker import MovieMaker
from src.Service.movie_service import MovieService
from src.DAO.db_connection import DBConnector
from typing import List


class MovieMakerTMDB:
    def __init__(self, db_conection: DBConnector):
        load_dotenv(override=True)
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.db_connection = db_conection
        self.movie_service = MovieService(db_conection)

    def get_some_movie_maker_infos_by_id(self, tmdb_id: int) -> List | None:
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
                return {"id_movie_maker": data['id'],
                        "adult" : data['adult'],
                        "name": data['name'],
                        "gender" : data['gender'],
                        "biography" : data['biography'],
                        "birthday" : data['birthday'],
                        "place_of_birth" : data['place_of_birth'],
                        "known_for_department" : data['known_for_department'],
                        "popularity" : data['popularity'],
                        "deathday" : data['deathday']
                }
            else:
                print(f"No MovieMaker found with TMDB ID : {tmdb_id}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None

    def get_some_movie_maker_infos_by_name(self, name: str) -> list[List] | None:
        # Reamarque : insomnia does not return thebiography, birthday, place of birth, deathday with this request.
        """
                Intermediate function that retrieves the information we are interested in for a movie maker on TMDB using its name. 
                Return a list with the id of the movie_maker an then a list of his know_for Movie.

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
            if 'results' in data and len(data['results']) > 0:
                results = data['results'] 
                movie_maker_results = []
                for result in results :
                    if result['known_for']:
                        movie_maker_results.append({
                            "id_movie_maker" : result['id'],
                            "known_for" : self.movie_service.create_movies(result['known_for'])
                        }
                        )
                return movie_maker_results
            else:
                print(f"No MovieMaker found with name : {name}.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error while fetching MovieMaker from TMDB: ", str(e))
            return None

    def get_movie_maker_by_name(self, name: str) -> list[MovieMaker] | None:
        if name:
            movie_maker_results = []
            results = self.get_some_movie_maker_infos_by_name(name)
            if results:
                for data in results:
                    id_movie_maker = data["id_movie_maker"]  # get the ID
                    result2 = self.get_some_movie_maker_infos_by_id(id_movie_maker) 
                    if result2:
                        data.update(result2)
                        movie_maker_results.append(MovieMaker(**data))  
            return movie_maker_results
        else:
            print("You have to enter a name")

    # def get_movie_maker_by_id(self, id_movie_maker: int) -> MovieMaker | None:
    #     if id_movie_maker:
    #         result = self.get_some_movie_maker_infos_by_id(id_movie_maker)
    #         if result:
    #             name_movie_maker = result['name']
    #             result2 = self.get_some_movie_maker_infos_by_name(name_movie_maker)  # pb de requete sql NONE
    #             for infos in result2 :
    #                 if infos['id_movie_maker'] == id_movie_maker:
    #                     result.update(infos) 
    #                     break
    #         return MovieMaker(**result)
    #     return None

# tmdb = MovieMakerTMDB()
# print(tmdb.get_some_movie_maker_infos_by_name("james cameron")) # peut pas être executer sans instance de db_connection
#print(tmdb.get_some_movie_maker_infos_by_id(2710))
#name = "James   Cameron"
#print(urllib.parse.quote(name))
#print(tmdb.get_movie_maker_by_name(name))
#print(tmdb.get_movie_maker_by_id(2710))


# # Ajouter ce bloc pour tester la recherche de "James Cameron"
# if __name__ == "__main__":
#     tmdb = MovieMakerTMDB()
#     movie_makers = tmdb.get_movie_maker_by_name_or_by_id("James Cameron")
#     if movie_makers:
#         for maker in movie_makers:
#             print(f"Found: {maker.name}, ID: {maker.id_movie_maker}")
#     else:
#         print("No movie makers found.")

""" known_for after request : look if it is possible to Movie()

{'backdrop_path': '/vL5LR6WdxWPjLPFRLe133jXWsh5.jpg', 
'id': 19995, Y 
'title': 'Avatar', Y
'original_title': 'Avatar', Y
'overview': Y 'In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.', 
'poster_path': '/kyeqWdyUXW608qlYkRqosgbbJyK.jpg',N
'media_type': 'movie', 
'adult': False Y, 
'original_language': 'en', Y
'genre_ids': [28, 12, 14, 878], Y
'popularity': 209.787, Y
'release_date': '2009-12-15', Y
'video': False, 
'vote_average': 7.6, Y
'vote_count': 31356 Y}

missing :
"belong to collection"
"budget"
"origine_country"
"revenu"
"runtime"

"""