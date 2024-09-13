# la clé API : fb0e5ded3d79bc5e571538030f7e5af8

import requests

def search_movie(api_key: str, query: str):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": query,
        "language": "en-US",
        "page": 1,
        "include_adult": "false"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        response.raise_for_status()

print(search_movie("fb0e5ded3d79bc5e571538030f7e5af8", "Twilight of the Warriors: Walled In" ))

# réponse
"""
print(search_movie("fb0e5ded3d79bc5e571538030f7e5af8", "Twilight of the Warriors: Walled In" )) : 

{'page': 1, 'results': [{'adult': False, 'backdrop_path': '/9juRmk8QjcsUcbrevVu5t8VZy5G.jpg',
'genre_ids': [28, 12, 80, 53], 'id': 923667, 'original_language': 'cn', 'original_title': '九龍城寨之圍城',
'overview': 'Set in the 1980s, troubled youth Chan Lok-kwun accidentally enters the Walled City,
discovers the order amidst its chaos, and learns important life lessons along the way. In the Walled City,
he becomes close friends with Shin, Twelfth Master and AV. Under the leadership of Cyclone,
they resist against the invasion of villain Mr. Big in a series of fierce battles.
Together, they vow to protect the safe haven that is Kowloon Walled City.', 'popularity': 918.486,
'poster_path': '/PywbVPeIhBFc33QXktnhMaysmL.jpg', 'release_date': '2024-04-23', 'title': 
'Twilight of the Warriors: Walled In', 'video': False, 'vote_average': 6.7, 'vote_count': 137}], 
'total_pages': 1, 'total_results': 1} """

# PywbVPeIhBFc33QXktnhMaysmL.jpg : c'est l'image de l'affiche du film

'''
print(search_movie("fb0e5ded3d79bc5e571538030f7e5af8", "The Smoke Master" )) : 

{'page': 1, 'results': [{'adult': False, 'backdrop_path': '/kwzNUM4yZ26XuNAPSyaWwJeWRP4.jpg', 
'genre_ids': [28, 35, 14], 'id': 950526, 'original_language': 'pt', 'original_title': 'O Mestre da Fumaça', 
'overview': 'The journey of Gabriel and Daniel, two brothers cursed by the Chinese mafia with its feared Three Generations Revenge, 
who have already reaped the life of their grandfather and their father. To survive, one of the brothers must learn the 
Smoke Style secrets, a little known Cannabis martial art, taught by a single master, high up in the mountains.', 
'popularity': 509.121, 'poster_path': '/mg6YkwftQOJjpT2ygYlCi11LWeC.jpg', 'release_date': '2023-05-18', 
'title': 'The Smoke Master', 'video': False, 'vote_average': 5.318, 'vote_count': 11}], 'total_pages': 1, 'total_results': 1}
'''
