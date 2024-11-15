import pytest

from src.Model.genre import Genre
from src.Service.genre_service import GenreService


@pytest.fixture
def genre_data():
    """Fixture pour fournir des données de genre."""
    return [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"},
    ]

#python -m pytest tests/Service/test_genre_service.py -k "test_create_list_of_genre_with_valid_data"
def test_create_list_of_genre_with_valid_data(genre_data):
    """Teste la création d'une liste de genres à partir de données valides."""
    genres = GenreService.create_list_of_genre(genre_data)

    assert len(genres) == 3
    assert all(isinstance(genre, Genre) for genre in genres)
    assert genres[0].id == 28
    assert genres[0].name == "Action"


def test_create_list_of_genre_with_empty_data():
    """Teste la création d'une liste vide lorsque les données sont vides."""
    genres = GenreService.create_list_of_genre([])

    assert genres == []
    assert len(genres) == 0


def test_create_list_of_genre_with_none_data():
    """Teste la création d'une liste vide lorsque les données sont None."""
    genres = GenreService.create_list_of_genre(None)

    assert genres == []
