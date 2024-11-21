import pytest

from src.Model.movie_maker import MovieMaker
from src.Service.movie_maker_service import MovieMakerService
from tests.DAO.test_db import MockDBConnection
from src.DAO.db_connection import DBConnector

#@pytest.fixture
#def movie_maker_data():
#    """Fixture pour fournir des données de collection de films."""
#    return {
#        movie_maker_dao = 
#        movie_maker_tmdb = 
        
#    }

def test_get_movie_maker_by_name_found_DB():
    # GIVEN
    moviemakerservice = MovieMakerService(DBConnector)

    # WHEN / THEN
    result = moviemakerservice.get_movie_maker_by_name( name = "Margaret Qualley")[0]
    assert result.id_movie_maker == 1392137

def test_get_movie_maker_by_name_found_TMDB():
    movieservice = MovieService(MockDBConnection)

    assert result.name == movie_maker.name


def test_get_movie_maker_by_name_not_found():
    movieservice = MovieService(MockDBConnection)

    """    movie_maker= MovieMaker(id_movie = 1392137,
                            adult = False,
                            biography = "Sarah Margaret Qualley (born October 23, 1994) is an American actress. The daughter of actress Andie MacDowell, she trained as a ballerina in her youth and briefly pursued a career in modeling. She made her acting debut with a minor role in the 2013 drama film Palo Alto and gained recognition for playing a troubled teenager in the HBO drama series The Leftovers (2014–2017). Qualley then appeared in the dark comedy The Nice Guys (2016) and in Netflix's supernatural thriller Death Note (2017).\n\nQualley gained acclaim and a nomination for a Primetime Emmy Award for portraying actress and dancer Ann Reinking in the FX biographical drama miniseries Fosse/Verdon (2019) and the title role in the Netflix drama miniseries Maid (2021). Her biggest commercial success came with Quentin Tarantino's comedy-drama Once Upon a Time in Hollywood (2019).",
                            gender= 1,
                            known_for_department = "Acting",
                            name = "Margaret Qualley",
                            place_of_birth= "Kalispell, Montana, USA",
                            popularity= 100.088)
    """
    result = movieservice.get_movie_maker_by_name("Clément Yvernault")

    assert result is None

    