from datetime import datetime
from src.DAO.user_follow_dao import UserFollowDao
from typing import Literal, Optional, Union
from src.DAO.db_connection import DBConnector



class MockDBConnectorFollowDAO(DBConnector):
    def __init__(self):
        super().__init__()  # Appel du constructeur de DBConnector (si nécessaire)
        self.data = {}  

    def sql_query(self, query: str, data: Optional[Union[tuple, list, dict]] = None, return_type: str = "one"):
        match query:
            case """
                SELECT COUNT(*) as count FROM follower
                WHERE id_user= %s AND id_user_followed = %s;
            """:
                id_user, id_user_followed = data
                if (id_user, id_user_followed) in self.data:
                    return {"count": 1}
                else:
                    return {"count": 0}
            case """
                    INSERT INTO follower (id_user, id_user_followed, date)
                    VALUES (%s, %s, %s);
                """:
                id_user, id_user_followed, the_date = data
                the_date = datetime.now().date()
                self.data[(id_user, id_user_followed)] = the_date
                return None
            case """
                SELECT * FROM follower
                WHERE id_user = %s;
            """:
                id_user = data[0]
                if id_user == 1:
                    return [
                        {"id_user": 1, "id_user_followed": 2},
                        {"id_user": 1, "id_user_followed": 3},
                        {"id_user": 1, "id_user_followed": 4},
                    ] 
                else:
                    return []
            case """
            DELETE FROM follower WHERE id_user = %s AND id_user_followed = %s
            """:
                id_user, id_user_followed = data
                if (id_user, id_user_followed) in self.data:
                    del self.data[(id_user, id_user_followed)] 
                    return None
            case _:
                raise ValueError(f"Unknown query: {query}")


def test_insert_follow():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_follow_dao = UserFollowDao(mock_db_connection)
    id_user = 1
    id_user_followed = 2
    user_follow_dao.insert(id_user, id_user_followed)
    assert (id_user, id_user_followed) in mock_db_connection.data, "Follow relationship should be inserted"
    assert mock_db_connection.data[(id_user, id_user_followed)] == datetime.now().date(), "Follow date should match"

def test_insert_follow_existing():
    mock_db_connection = MockDBConnectorFollowDAO()
    mock_db_connection.data[(1, 2)] = datetime.now().date()
    user_follow_dao = UserFollowDao(mock_db_connection)
    id_user = 1
    id_user_followed = 2
    user_follow_dao.insert(id_user, id_user_followed)
    assert len(mock_db_connection.data) == 1, "No new relationship should be added"

def test_get_all_user_followed():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_follow_dao = UserFollowDao(mock_db_connection)
    id_user = 1
    followed_users = user_follow_dao.get_all_user_followed(id_user)
    assert followed_users == [2, 3, 4], "The followed users list should contain users 2, 3, and 4"

def test_get_all_user_followed_no_followers():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_follow_dao = UserFollowDao(mock_db_connection)
    id_user = 999
    followed_users = user_follow_dao.get_all_user_followed(id_user)
    assert followed_users is None, "If the user follows no one, the result should be None"

def test_delete_follow_existing():
    mock_db_connection = MockDBConnectorFollowDAO()
    mock_db_connection.data[(1, 2)] = datetime.now().date()
    user_follow_dao = UserFollowDao(mock_db_connection)
    result = user_follow_dao.delete(1, 2)
    assert result is None, "The follow relationship should be deleted."

def test_is_following_existing():
    mock_db_connection = MockDBConnectorFollowDAO()
    mock_db_connection.data[(1, 2)] = datetime.now().date()  # Simule une relation existante
    user_follow_dao = UserFollowDao(mock_db_connection)
    is_following = user_follow_dao.is_following(1, 2)
    assert is_following, "is_following devrait retourner True pour une relation existante"

def test_is_following_non_existing():
    mock_db_connection = MockDBConnectorFollowDAO()
    user_follow_dao = UserFollowDao(mock_db_connection)
    is_following = user_follow_dao.is_following(1, 3)  # Pas de relation (1, 3) dans les données mock
    assert not is_following, "is_following devrait retourner False pour une relation inexistante"





