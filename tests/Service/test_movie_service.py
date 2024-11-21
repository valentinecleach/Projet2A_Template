import pytest

from src.DAO.db_connection import DBConnector
from src.Service.movie_service import MovieService
from tests.DAO.test_db import MockDBConnection

# ------ TEST GET MOVIE BY ID -----------


def test_get_movie_by_id_found_in_db():
    """Test method get_movie_by_id when the id is found in the database"""
    # GIVEN
    movieservice = MovieService(DBConnector)

    # WHEN
    result = movieservice.get_movie_by_id(19995)

    # THEN
    assert result.title == "Avatar"


def test_get_movie_by_id_found_in_tmdb():
    # GIVEN
    movieservice = MovieService(MockDBConnection)

    # Verifie que ce nest pas dans la DAO
    assert movieservice.movie_dao.get_by_id(19995) is None

    # WHEN
    result = movieservice.get_movie_by_id(19995)
    # THEN
    assert result.title == "Avatar"


def test_get_movie_by_id_not_found():
    # GIVEN
    movieservice = MovieService(MockDBConnection)

    # WHEN / THEN
    # Vérification du mock pour ne trouver le film ni dans la base de données
    # ni dans TMDB
    assert movieservice.movie_dao.get_by_id(999) is None
    assert movieservice.movie_tmdb.get_movie_by_id(999) is None

    result = movieservice.get_movie_by_id(999)

    assert result is None


# ------ GET MOVIE BY TITLE -----------


def test_get_movie_by_title_in_db():
    """Tests the method get_movie_by_title if the title is found in the database.
    Since the method returns a list of films under the same or similar title,
    we will select only the first one.
    """
    # GIVEN
    movieservice = MovieService(DBConnector)

    # WHEN
    result = movieservice.get_movie_by_title("Avatar")[0]

    # THEN
    assert result.id_movie == 19995


def test_get_movie_by_title_in_tmdb():
    # GIVEN
    movieservice = MovieService(MockDBConnection)

    # Verifie que ce nest pas dans la DAO
    assert movieservice.movie_dao.get_by_title("Avatar") is None

    # WHEN
    result = movieservice.get_movie_by_title("Avatar")[0]

    # THEN
    assert result.id_movie == 19995


def test_get_movie_by_title_not_found():
    # GIVEN
    movieservice = MovieService(MockDBConnection)

    # WHEN / THEN
    # Vérification du mock pour ne trouver le film ni dans la base de données ni dans TMDB
    assert movieservice.movie_dao.get_by_title("The Joyful Christmas Exam") is None
    assert (
        movieservice.movie_tmdb.get_movies_by_title("The Joyful Christmas Exam") is None
    )

    result = movieservice.get_movie_by_title("The Joyful Christmas Exam")

    assert result is None


# ------ CREATE MOVIES -----------
def test_create_movies():
    # GIVEN
    movieservice = MovieService(MockDBConnection)

    movie_data = [{"id": 19995}]

    # WHEN / THEN
    list_movies = movieservice.create_movies(movie_data)[0]

    assert list_movies.title == "Avatar"


"""
movie = Movie(
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
    """
