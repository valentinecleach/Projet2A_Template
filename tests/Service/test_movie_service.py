import datetime
from unittest.mock import MagicMock

import pytest

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.Model.genre import Genre
from src.Model.movie import Movie
from src.Model.movie_collection import MovieCollection
from src.Service.movie_service import MovieService
from src.TMDB.movie_tmdb import MovieTMDB


def test_get_movie_by_id_found_in_db():
    """
    Test si le film est trouvé dans la base de données.
    """
    db_connection = DBConnector()
    movie_dao_mock = MagicMock(spec=MovieDAO)
    movie_tmdb_mock = MagicMock(spec=MovieTMDB)

    movie_service = MovieService(db_connection)
    movie_service.movie_dao = movie_dao_mock
    movie_service.movie_tmdb = movie_tmdb_mock

    expected_movie = Movie(id=1, title="Inception", genre_ids=[28, 878])
    movie_dao_mock.get_by_id.return_value = expected_movie

    result = movie_service.get_movie_by_id(1)
    print(result)
    assert (
        result == expected_movie
    )  # Vérifie que le film retourné correspond à celui attendu.
