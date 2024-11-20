import datetime
from typing import Optional

import pytest

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.Model.genre import Genre
from src.Model.movie import Movie
from src.Model.movie_collection import MovieCollection
from src.Service.movie_service import MovieService
from src.TMDB.movie_tmdb import MovieTMDB
from tests.DAO.test_db import MockDBConnection

# ------ TEST GET MOVIE BY ID -----------


def test_get_movie_by_id_found_in_db():

    # GIVEN
    movieservice = MovieService(DBConnector)

    # Configuration du mock pour retourner un film de la base de données
    mock_movie = Movie(
        id_movie=19995,
        title="Avatar",
        belongs_to_collection=[MovieCollection(id=87096, name="Avatar Collection")],
        budget=237000000,
        genres=[
            Genre(id=28, name="Action"),
            Genre(id=12, name="Adventure"),
            Genre(id=14, name="Fantasy"),
            Genre(id=878, name="Science Fiction"),
        ],
        origin_country=["US"],
        original_language="en",
        original_title="Avatar",
        overview="In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
        popularity=99.959,
        release_date=datetime.date(2009, 12, 15),
        revenue=2923706026,
        runtime=162,
        vote_average=7.582,
        vote_count=31385,
        adult=False,
    )

    # WHEN
    result = movieservice.get_movie_by_id(19995)

    # THEN
    assert result == mock_movie


def test_get_movie_by_id_found_in_tmdb(movie_service):
    service, movie_dao_mock, movie_tmdb_mock = movie_service

    # Configuration du mock pour retourner None de la base de données et un film de TMDB
    movie_dao_mock.get_by_id.return_value = None
    mock_movie_tmdb = Movie(id=1, title="The Matrix Reloaded", year=2003)
    movie_tmdb_mock.get_movie_by_id.return_value = mock_movie_tmdb

    result = service.get_movie_by_id(1)

    assert result == mock_movie_tmdb
    movie_dao_mock.get_by_id.assert_called_once_with(1)
    movie_tmdb_mock.get_movie_by_id.assert_called_once_with(1)
    movie_dao_mock.insert.assert_called_once_with(mock_movie_tmdb)


def test_get_movie_by_id_not_found(movie_service):
    service, movie_dao_mock, movie_tmdb_mock = movie_service

    # Configuration du mock pour ne trouver le film ni dans la base de données ni dans TMDB
    movie_dao_mock.get_by_id.return_value = None
    movie_tmdb_mock.get_movie_by_id.return_value = None

    result = service.get_movie_by_id(999)

    assert result is None
    movie_dao_mock.get_by_id.assert_called_once_with(999)
    movie_tmdb_mock.get_movie_by_id.assert_called_once_with(999)


# ------ GET MOVIE BY TITLE -----------

# ------ CREATE MOVIES -----------

# ------ GET MOVIE BY ID -----------
