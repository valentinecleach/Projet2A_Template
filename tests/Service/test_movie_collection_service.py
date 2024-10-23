import pytest

from src.Model.movie_collection import MovieCollection
from src.Service.movie_collection_service import MovieCollectionService


@pytest.fixture
def movie_collection_data():
    """Fixture pour fournir des données de collection de films."""
    return {
        "id": 87096,
        "name": "Avatar Collection",
        "poster_path": "/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg",
    }


def test_create_list_of_collection_with_valid_data(movie_collection_data):
    """Teste la création d'une instance MovieCollection avec des données valides."""
    collection = MovieCollectionService.create_list_of_collection(movie_collection_data)

    assert isinstance(collection, list)
    assert len(collection) == 1
    assert isinstance(collection[0], MovieCollection)
    assert collection[0].id == 87096
    assert collection[0].name == "Avatar Collection"


def test_create_list_of_collection_with_empty_data():
    """Teste la création d'une collection avec des données vides."""
    collection = MovieCollectionService.create_list_of_collection({})

    assert collection is None


def test_create_list_of_collection_with_none_data():
    """Teste la création d'une collection avec des données None."""
    collection = MovieCollectionService.create_list_of_collection(None)

    assert collection is None
