import pytest

# Movie 

@pytest.fixture
def avatar():
    return {
    "id_movie": 19995,
    "title": "Avatar",
    "adult": False,
    "belongs_to_collection": None ,
    "budget": 237000000,
    "genre": None,
    "origine_country": ["US"],
    "original_language": "en",
    "original_title": "Avatar",
    "overview": "In the 22nd century, a paraplegic Marine is dispatched to the moon "
                 "Pandora on a unique mission, but becomes torn between following orders "
                 "and protecting an alien civilization.",
    "popularity": 100.088,
    "release_date": "2009-12-15",
    "revenue": 2923706026,
    "runtime": 162,
    "vote_average": 7.582,
    "vote_count": 31290,
}


@pytest.fixture
def titanic():
    return {
    "id_movie": 597,
    "title": "Titanic",
    "adult": False,
    "belongs_to_collection": None,
    "budget": 200000000,
    "genre": [
        {"id": 18, "name": "Drama"},
        {"id": 10749, "name": "Romance"}
    ],
    "origine_country": ["US"],
    "original_language": "en",
    "original_title": "Titanic",
    "overview": ("101-year-old Rose DeWitt Bukater tells the story of her life "
                 "aboard the Titanic, 84 years later. A young Rose boards the ship "
                 "with her mother and fiancé. Meanwhile, Jack Dawson and Fabrizio De Rossi "
                 "win third-class tickets aboard the ship. Rose tells the whole story from "
                 "Titanic's departure through to its death—on its first and last voyage—"
                 "on April 15, 1912."),
    "popularity": 121.592,
    "release_date": "1997-11-18",
    "revenue": 2264162353,
    "runtime": 194,
    "vote_average": 7.906,
    "vote_count": 25134
}


# MovieMaker

@pytest.fixture
def james_cameron():
    return {
        'id_movie_maker': 2710,
        'adult': False,
        'name': "James Cameron",
        'gender': 2,
        'biography': "Famous director of Titanic and Avatar.",
        'birthday': "1954-08-16",
        'place_of_birth': "Kapuskasing, Ontario, Canada",
        'deathday': None,
        'known_for_department': "Directing",
        'popularity': 19.057,
        'known_for': [avatar, titanic]
    }
