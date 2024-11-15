import pytest
from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.movie_dao import MovieDAO
from datetime import date
from src.Model.movie import Movie
from tests.conftest import avatar  # Assurez-vous que `avatar` est bien défini ici

class MockMovieDBConnector:
    def __init__(self, movie=None):
        self.movie = movie or avatar  # Utilise l'avatar si aucun film n'est fourni

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "one",
    ):
        match query:
            case "SELECT * FROM movie WHERE id_movie=%s":
                if not data:
                    raise Exception("No data provided.")
                id_movie = data[0]  # Récupère l'ID à partir de la donnée
                if id_movie == 19995:
                    return Movie(**self.movie)
        return None  # Pour d'autres requêtes non définies

@pytest.fixture
def mock_db_connection():
    return MockMovieDBConnector()

# NE MARCHE PAS
# python -m pytest tests/DAO/test_movie_dao.py -k 'test_get_movie_by_id'
def test_get_movie_by_id(mock_db_connection):
    movie_dao = MovieDAO(mock_db_connection)
    movie = movie_dao.get_by_id(19995)
    
    assert movie is not None # -> assert None is not None
    assert movie.id_movie == 19995
    assert movie.title == "Avatar"
    assert movie.adult is False
    assert movie.budget == 237000000

# MARCHE
# python -m pytest tests/DAO/test_movie_dao.py -k 'test_get_movie_by_non_existent_id'
def test_get_movie_by_non_existent_id(mock_db_connection):
    movie_dao = MovieDAO(mock_db_connection)
    movie = movie_dao.get_by_id(99999)  # ID qui n'existe pas
    
    assert movie is None  # Vérifiez que la méthode renvoie None pour un film inexistant
