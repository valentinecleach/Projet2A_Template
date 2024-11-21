from src.DAO.db_connection import DBConnector
from src.Service.recommend_service import RecommendService
from tests.DAO.test_db import MockDBConnection


def test_find_users_to_follow_no_id():
    recommendservice = RecommendService(DBConnector)
    assert recommendservice.find_users_to_follow() is None


def test_find_users_to_follow_users_found():
    recommendservice = RecommendService(DBConnector)

    users = recommendservice.find_users_to_follow(id_user = )
    
    result = recommendservice.find_users_to_follow(id_user)
    
    assert result == 


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(DBConnector)

    id_user = 
    
    users = recommendservice.find_users_to_follow(id_user)
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    result = recommendservice.find_users_to_follow(id_user)
    
    assert result == 


def test_find_users_to_follow_no_users_and_popular():
    recommendservice = RecommendService(DBConnector)
    id_user = 
    
    users = recommendservice.find_users_to_follow(id_user)
    
    assert recommendservice.recommend_dao.recommend_users_to_follow(id_user) is None
    assert recommendservice.recommend_dao.get_popular_users(id_user) is None
    
    result = recommendservice.find_users_to_follow(id_user)
    
    assert result is None 



def test_find_movie_to_collect():
    pass
