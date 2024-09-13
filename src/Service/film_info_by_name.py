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

