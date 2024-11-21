import pytest

from src.DAO.db_connection import DBConnector
from src.Service.movie_maker_service import MovieMakerService
from tests.DAO.test_db import MockDBConnection


def test_get_movie_maker_by_name_found_DB():
    # GIVEN
    moviemakerservice = MovieMakerService(DBConnector)

    # WHEN / THEN
    result = moviemakerservice.get_movie_maker_by_name(name="Margaret Qualley")[0]
    assert result.id_movie_maker == 1392137


def test_get_movie_maker_by_name_found_TMDB():
    # GIVEN
    moviemakerservice = MovieMakerService(MockDBConnection)
    assert (
        moviemakerservice.movie_maker_dao.get_by_name(name="Margaret Qualley") == None
    )

    # WHEN
    result = moviemakerservice.get_movie_maker_by_name(name="Margaret Qualley")[0]
    # THEN
    assert result.id_movie_maker == 1392137


def test_get_movie_maker_by_name_not_found():
    # GIVEN
    moviemakerservice = MovieMakerService(MockDBConnection)
    assert (
        moviemakerservice.movie_maker_dao.get_by_name(name="Clément Yvernault") is None
    )
    assert (
        moviemakerservice.movie_maker_tmdb.get_movie_maker_by_name(
            name="Clément Yvernault"
        )
        == []
    )

    # WHEN
    result = moviemakerservice.get_movie_maker_by_name(name="Clément Yvernault")

    # THEN
    assert result is None
