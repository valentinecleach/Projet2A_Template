import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.DAO.comment_dao import CommentDao
from src.Model.comment import Comment
from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class TestCommentDao(unittest.TestCase):

    @patch("src.DAO.comment_dao.DBConnection")
    @patch("src.DAO.user_dao.UserDao.get_user_by_id")
    @patch("src.DAO.movie_dao.MovieDAO.get_by_id")
    def test_insert_comment(
        self, mock_get_movie_by_id, mock_get_user_by_id, mock_db_connection
    ):
        # Mock database connection and cursor
        mock_connection = mock_db_connection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value
        mock_cursor.execute.return_value = 1  # Simulate successful insert
        mock_connection.connection.commit.return_value = None

        # Mock user and movie retrieval
        mock_user = ConnectedUser(id=1, name="John Doe")
        mock_movie = Movie(id=1, title="The Matrix")
        mock_get_user_by_id.return_value = mock_user
        mock_get_movie_by_id.return_value = mock_movie

        # Instantiate CommentDao and call insert
        dao = CommentDao()
        result = dao.insert(1, 1, "Amazing movie!")

        # Assert that the SQL insert query was executed
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO comment(id_user, id_movie, comments, date) VALUES (%s, %s, %s, %s)",
            (1, 1, "Amazing movie!", mock.ANY),  # mock.ANY for the datetime field
        )

        # Assert that the result is an instance of Comment
        self.assertIsInstance(result, Comment)
        self.assertEqual(result.comment, "Amazing movie!")
        self.assertEqual(result.user, mock_user)
        self.assertEqual(result.movie, mock_movie)

        # Check if the commit was called
        mock_connection.connection.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
