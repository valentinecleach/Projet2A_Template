import unittest
from unittest.mock import MagicMock, patch

from src.DAO.genre_dao import GenreDao
from src.Model.genre import Genre


class TestGenreDao(unittest.TestCase):

    @patch('src.DAO.db_connection.DBConnection')
    def setUp(self, MockDBConnection):
        # Create a mock DB connection
        self.mock_db_connection = MockDBConnection.return_value
        self.genre_dao = GenreDao()

    def test_insert_success(self):
        # Arrange
        new_genre = Genre(id=28, name="Action")
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Set up the connection and cursor mocks
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        self.mock_db_connection.connection.__enter__.return_value = mock_connection

        # Act
        self.genre_dao.insert(new_genre)

        # Assert
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO Genre (id_genre, name_genre)
            VALUES (%s, %s)
            """,
            (new_genre.id, new_genre.name)
        )
        mock_connection.commit.assert_called_once()

    def test_insert_error(self):
        # Arrange
        new_genre = Genre(id=28, name="Action")
        self.mock_db_connection.connection.__enter__.return_value.cursor.return_value.__enter__.side_effect = Exception("Database error")

        # Act
        with self.assertLogs(level='INFO') as log:
            self.genre_dao.insert(new_genre)

        # Assert
        self.assertIn("Insertion error : Database error", log.output[0])

if __name__ == '__main__':
    unittest.main()



