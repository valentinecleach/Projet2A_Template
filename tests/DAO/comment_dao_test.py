import unittest
from unittest.mock import patch

from src.DAO.comment_dao import CommentDao
from src.Model.comment import Comment


class TestCommentDao(unittest.TestCase):

    @patch("src.DAO.comment_dao.DBConnection")
    def test_insert_comment(self, MockDBConnection):
        # Mock database behavior
        mock_connection = MockDBConnection.return_value
        mock_connection.insert.return_value = True

        # Test the insert method
        dao = CommentDao()
        result = dao.insert(1, 1, "Great movie!")

        # Verify if the insert method was called with correct parameters
        mock_connection.insert.assert_called_once_with(
            "cine.comment", (1, 1, "Great movie!", unittest.mock.ANY)
        )

        # Ensure the result is a Comment instance
        self.assertIsInstance(result, Comment)
        self.assertEqual(result.comment, "Great movie!")

    @patch("src.DAO.comment_dao.DBConnection")
    def test_get_user_comment(self, MockDBConnection):
        # Mock data returned from database
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {"id_user": 1, "id_movie": 1, "date": "2023-01-01", "comment": "Good!"}
        ]

        # Test the get_user_comment method
        dao = CommentDao()
        comments = dao.get_user_comment(1, 1)

        # Check if the return value is correct
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].comment, "Good!")

    @patch("src.DAO.comment_dao.DBConnection")
    def test_delete_comment(self, MockDBConnection):
        # Mock the DB connection for delete operation
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value

        # Create a Commen
