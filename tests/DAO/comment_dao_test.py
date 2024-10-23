import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.DAO.comment_dao import CommentDao
from src.Model.comment import Comment


class TestCommentDao(unittest.TestCase):

    @patch("src.DAO.comment_dao.DBConnection")
    def test_insert_comment(self, MockDBConnection):
        # Mock database connection and cursor
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value
        mock_cursor.execute.return_value = 1  # Simulate successful insert
        mock_connection.connection.commit.return_value = None

        # Test the insert method
        dao = CommentDao()
        result = dao.insert(1, 1, "Great movie!")

        # Check if the insert query was called
        mock_cursor.execute.assert_called_once()

        # Ensure the result is a Comment instance
        self.assertIsInstance(result, Comment)
        self.assertEqual(result.comment, "Great movie!")

    @patch("src.DAO.comment_dao.DBConnection")
    def test_get_user_comment(self, MockDBConnection):
        # Mock data returned from database
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {"id_user": 1, "id_movie": 1, "date": datetime.now(), "comment": "Good!"}
        ]

        # Test the get_user_comment method
        dao = CommentDao()
        comments = dao.get_user_comment(1, 1)

        # Ensure comments is a list and not empty
        self.assertIsInstance(comments, list)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].comment, "Good!")

    @patch("src.DAO.comment_dao.DBConnection")
    def test_get_recent_comments(self, MockDBConnection):
        # Mock data returned from database
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {"id_user": 1, "id_movie": 1, "date": datetime.now(), "comment": "Amazing!"}
        ]

        # Test the get_recent_comments method
        dao = CommentDao()
        comments = dao.get_recent_comments(1)

        # Ensure comments is a list and not empty
        self.assertIsInstance(comments, list)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].comment, "Amazing!")

    @patch("src.DAO.comment_dao.DBConnection")
    def test_delete_comment(self, MockDBConnection):
        # Mock the DB connection for delete operation
        mock_connection = MockDBConnection.return_value
        mock_cursor = mock_connection.connection.cursor.return_value

        # Create a mock comment
        comment = Comment(
            user=MagicMock(),
            movie=MagicMock(),
            date=datetime.now(),
            comment="To delete",
        )

        # Test the delete method
        dao = CommentDao()
        dao.delete(comment)

        # Ensure the delete query was executed
        mock_cursor.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
