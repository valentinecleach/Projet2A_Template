##### Marche passsssssssssssssssssssssss !!!! ####
from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.movie_dao import MovieDAO
import pytest

if TYPE_CHECKING:
    from src.Model.movie import Movie

class MockMovieDBConnector:
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
                id_movie = data[0]
                # Simuler les données pour le film "Avatar"
                if id_movie == 19995:
                    return {
                        "id_movie": 19995,
                        "title": "Avatar",
                        "adult": False,
                        "budget": 237000000,
                        # Ajoute d'autres champs nécessaires si nécessaire
                    }
        return None  # Pour d'autres requêtes non définies

@pytest.fixture
def mock_db_connection():
    return MockMovieDBConnector()

def test_get_movie_by_id(mock_db_connection, avatar):
    movie_dao = MovieDAO(mock_db_connection)
    movie: Movie = movie_dao.get_by_id(19995)
    
    assert movie is not None
    assert movie.id_movie == 19995
    assert movie.title == "Avatar"
    assert movie.adult is False
    assert movie.budget == 237000000
