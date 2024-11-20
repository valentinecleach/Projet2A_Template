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


def test_create_list_of_genre_with_invalid_data_type():
    """Teste la gestion des données avec un type incorrect."""
    with pytest.raises(TypeError):
        GenreService.create_list_of_genre("not a list")


def test_create_list_of_genre_with_missing_keys():
    """Teste la création de genres lorsque certaines clés sont manquantes."""
    data_with_missing_keys = [
        {"id": 28},  # Pas de "name"
        {"name": "Adventure"},  # Pas de "id"
    ]

    with pytest.raises(KeyError):
        GenreService.create_list_of_genre(data_with_missing_keys)


def test_create_list_of_genre_with_extra_keys(genre_data):
    """Teste la création de genres avec des données contenant des clés supplémentaires."""
    data_with_extra_keys = [
        {"id": 28, "name": "Action", "description": "A genre with lots of explosions"},
        {"id": 12, "name": "Adventure", "popularity": 9.5},
    ]

    genres = GenreService.create_list_of_genre(data_with_extra_keys)

    assert len(genres) == 2
    assert all(isinstance(genre, Genre) for genre in genres)
    assert genres[0].id == 28
    assert genres[0].name == "Action"
