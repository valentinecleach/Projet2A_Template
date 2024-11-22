from datetime import datetime
from src.DAO.user_favorites_dao import UserFavoriteDao
from typing import Optional, Union
from src.DAO.db_connection import DBConnector


class MockDBConnectorFavoriteDAO(DBConnector):
    def __init__(self):
        super().__init__()  # Appel du constructeur de DBConnector (si nécessaire)
        self.data = {}

    def sql_query(self, query: str, data: Optional[Union[tuple, list, dict]] = None, return_type: str = "one"):
        match query:
            case """
                SELECT COUNT(*) as count FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """:
                id_user, id_movie = data
                if (id_user, id_movie) in self.data:
                    return {"count": 1}
                else:
                    return {"count": 0}
            case """
                    INSERT INTO user_movie_collection (id_user, id_movie, date)
                    VALUES (%s, %s, %s);
                """:
                id_user, id_movie, the_date = data
                the_date = datetime.now().date()
                self.data[(id_user, id_movie)] = the_date
                return None
            case """
                SELECT id_movie, date FROM user_movie_collection
                WHERE id_user = %s
                ORDER BY date DESC;
            """:
                id_user = data[0]
                if id_user == 1:
                    return [
                        {"id_user": 1, "id_movie": 101},
                        {"id_user": 1, "id_movie": 102},
                        {"id_user": 1, "id_movie": 103},
                    ] 
                else:
                    return []
            case """
                DELETE FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """:
                id_user, id_movie = data
                if (id_user, id_movie) in self.data:
                    del self.data[(id_user, id_movie)]
                    return None
            case _:
                raise ValueError(f"Unknown query: {query}")


def test_insert_favorite():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    id_user = 1
    id_movie = 101
    user_favorite_dao.insert(id_user, id_movie)
    assert (id_user, id_movie) in mock_db_connection.data, "Favorite relationship should be inserted"
    assert mock_db_connection.data[(id_user, id_movie)] == datetime.now().date(), "Favorite date should match"

def test_insert_favorite_existing():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    mock_db_connection.data[(1, 101)] = datetime.now().date()  # Simule une relation existante
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    id_user = 1
    id_movie = 101
    user_favorite_dao.insert(id_user, id_movie)
    assert len(mock_db_connection.data) == 1, "No new favorite relationship should be added"

def test_get_user_favorites():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    id_user = 1
    favorites = user_favorite_dao.get_favorites(id_user)
    assert favorites == [101, 102, 103], "The list of favorite movies should be [101, 102, 103]"

def test_get_user_favorites_no_favorites():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    id_user = 999
    favorites = user_favorite_dao.get_favorites(id_user)
    assert favorites is None, "If the user has no favorites, the result should be None"

def test_remove_favorite_existing():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    mock_db_connection.data[(1, 101)] = datetime.now().date()  
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    result = user_favorite_dao.remove(1, 101)
    assert result is None, "Favorite relationship should be deleted"

def test_remove_favorite_non_existing():
    mock_db_connection = MockDBConnectorFavoriteDAO()
    user_favorite_dao = UserFavoriteDao(mock_db_connection)
    result = user_favorite_dao.remove(1, 999) 
    assert result is None, "No error should occur when trying to remove a non-existing favorite"

