import pytest

from src.DAO.db_connection import DBConnector
from src.Service.recommend_service import RecommendService
from tests.DAO.test_db import MockDBConnection

### FIND USERS TO FOLLOW ###


def test_find_users_to_follow_users_found():
    # GIVEN
    recommendservice = RecommendService(MockDBConnection)
    id_user = 1

    # WHEN
    result = recommendservice.find_users_to_follow(id_user)[0]

    # THEN
    assert result.id_user == 2


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(DBConnector)
    id_user = 1
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    result = recommendservice.find_users_to_follow(id_user)[0]
    
    assert result.id_user == 2


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(MockDBConnection)
    id_user = 1
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    assert recommendservice.recommend_dao.get_popular_users(id_user) is None
    
    result = recommendservice.find_users_to_follow(id_user)
    
    assert result is None 

### FIND MOVIE TO COLLECT ###

def test_find_movie_to_collect_no_id():
    recommendservice = RecommendService(DBConnector)
    assert recommendservice.find_movie_to_collect() is None


def test_find_movie_to_collect_movies_found():
    recommendservice = RecommendService(DBConnector)

    movies = recommendservice.find_movie_to_collect(id_user = 217)
    
    result = recommendservice.find_movie_to_collect(id_user)[0]
    
    assert result.id_movie == 19965


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(DBConnector)

    id_user = 217
    
    users = recommendservice.find_movie_to_collect(id_user)
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    result = recommendservice.find_movie_to_collect(id_user)[0]
    
    assert result.id_movie == 19965


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(DBConnector)
    id_user = 217
    
    users = recommendservice.find_movie_to_collect(id_user)
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    assert recommendservice.recommend_dao.get_popular_users(id_user) is None
    
    result = recommendservice.find_users_to_follow(id_user)
    
    assert result is None 

