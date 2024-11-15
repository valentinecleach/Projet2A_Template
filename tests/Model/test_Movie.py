import pytest
from pydantic_core import ValidationError

from src.Model.movie import Movie
from tests.conftest import avatar, titanic

# Des fixtures sont définies dans le fichier conftest


@pytest.mark.parametrize(
    "kwargs, erreur, message_erreur",
    [
        ({"id_movie": -1}, ValueError, "The id needs to be a positive integer"),
        ({"title": 123}, TypeError, "The title must be a string"
        ),
        (
            {"belongs_to_collection": "not_a_dict"},
            TypeError,
            "belongs_to_collection must be a dictionary.",
        ),
        ({"budget": -1000.0}, ValueError, "budget must be a positive float."),
        ({"genre": "not_a_list"}, TypeError, "genre must be a list of Genre objects."),
        ({"genre": []}, TypeError, "Each genre must be a Genre object."),
        ({"origine_country": 123}, TypeError, "origine_country must be a string."),
        (
            {"release_date": "invalid-date"},
            ValueError,
            "release_date must be in the format YYYY-MM-DD.",
        ),
        ({"popularity": "not_a_float"}, TypeError, "popularity must be a float."),
        ({"runtime": "not_a_float"}, TypeError, "runtime must be a float."),
        ({"vote_average": "not_a_float"}, TypeError, "vote_average must be a float."),
        ({"vote_count": "not_an_int"}, TypeError, "vote_count must be an integer."),
        ({"adult": "not_a_bool"}, TypeError, "adult must be a boolean."),
        ({"adult": True}, ValueError, "The film can't be an adult film."),
    ],
)
#python -m pytest tests/Model/test_Movie.py -k "test_movie_init_echec"
def test_movie_init_echec(titanic, kwargs, erreur, message_erreur):
    # Mettre à jour titanic avec les arguments testés
    test_kwargs = titanic.copy()  # Créer une copie pour éviter de modifier la fixture
    test_kwargs.update(kwargs)  # Mettre à jour avec les arguments invalides
    with pytest.raises(erreur, match=message_erreur):
        Movie(**test_kwargs)

# python -m pytest tests/Model/test_Movie.py -k "test_movie_constructor_ok"
def test_movie_constructor_ok():
    the_shining = Movie(id_movie=12, original_title="The Shining")
    assert the_shining.id_movie == 12
    assert the_shining.original_title == "The Shining"


def test_movie_constructor_throws_on_incorrect_input():
    with pytest.raises(ValidationError) as exception_info:
        Movie(id="Twelve", original_title="Dracula")
    assert "id" in str(
        exception_info.value
    ) and "Input should be a valid integer, unable to parse string as an integer" in str(
        exception_info.value
    )
