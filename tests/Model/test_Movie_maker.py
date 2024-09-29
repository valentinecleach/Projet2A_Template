from Model.MovieMaker import MovieMaker
from tests.conftest import avatar, titanic
import pytest

def test_movie_maker_constructor_ok(movie_maker_data):
    movie_maker = MovieMaker(**movie_maker_data)
    assert movie_maker.id_movie_maker == 2710
    assert movie_maker.name == "James Cameron"
    assert len(movie_maker.known_for) == 2  # Vérifie qu'il y a bien 2 films
    assert movie_maker.known_for[0]['title'] == "Avatar"  # Vérifie le premier film
    assert movie_maker.known_for[1]['title'] == "Titanic"  # Vérifie le deuxième film