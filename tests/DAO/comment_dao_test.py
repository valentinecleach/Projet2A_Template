from datetime import datetime

import pytest

from src.DAO.comment_dao import CommentDao
from src.DAO.db_connection import DBConnection
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment


@pytest.fixture(scope="module")
def setup_db():
    """Fixture to set up a test environment and clean up after tests."""
    connection = DBConnection().connection
    cursor = connection.cursor()

    # Create tables for testing if not exists
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL
    )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL
    )"""
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY,
        id_user INT REFERENCES users(id),
        id_movie INT REFERENCES movies(id),
        comments TEXT,
        date TIMESTAMP
    )"""
    )
    connection.commit()

    # Clean up database after all tests
    yield
    cursor.execute("DELETE FROM comments")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM movies")
    connection.commit()
    cursor.close()


@pytest.fixture
def insert_test_data(setup_db):
    """Insert test data for users and movies."""
    connection = DBConnection().connection
    cursor = connection.cursor()

    # Insert a test user and a test movie
    cursor.execute(
        "INSERT INTO users (username) VALUES (%s) RETURNING id", ("test_user",)
    )
    id_user = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO movies (title) VALUES (%s) RETURNING id", ("test_movie",)
    )
    id_movie = cursor.fetchone()[0]

    connection.commit()

    yield id_user, id_movie

    cursor.execute(
        "DELETE FROM comments WHERE id_user = %s AND id_movie = %s", (id_user, id_movie)
    )
    connection.commit()
    cursor.close()


def test_insert_comment(insert_test_data):
    """Test inserting a comment into the database."""
    id_user, id_movie = insert_test_data

    # Create an instance of CommentDao
    dao = CommentDao()

    # Insert a comment
    comment_text = "Great movie!"
    comment = dao.insert(id_user, id_movie, comment_text)

    # Ensure the returned comment is not None
    assert comment is not None
    assert isinstance(comment, Comment)
    assert comment.comment == comment_text
    assert comment.movie.id == id_movie
    assert comment.user.id == id_user


def test_get_user_comment(insert_test_data):
    """Test fetching a user's comment on a movie."""
    id_user, id_movie = insert_test_data

    # Create an instance of CommentDao
    dao = CommentDao()

    # Insert a comment for the test
    dao.insert(id_user, id_movie, "Awesome movie!")

    # Fetch the user's comment
    comments = dao.get_user_comment(id_user, id_movie)

    # Ensure the returned comment is correct
    assert len(comments) > 0
    assert isinstance(comments[0], Comment)
    assert comments[0].comment == "Awesome movie!"


def test_get_recent_comments(insert_test_data):
    """Test fetching recent comments."""
    id_user, id_movie = insert_test_data

    # Create an instance of CommentDao
    dao = CommentDao()

    # Insert a comment
    dao.insert(id_user, id_movie, "Amazing movie!")

    # Fetch recent comments for the movie
    comments = dao.get_recent_comments(id_movie)

    # Ensure the comment is fetched correctly
    assert len(comments) > 0
    assert isinstance(comments[0], Comment)
    assert comments[0].comment == "Amazing movie!"


def test_delete_comment(insert_test_data):
    """Test deleting a comment."""
    id_user, id_movie = insert_test_data

    # Create an instance of CommentDao
    dao = CommentDao()

    # Insert a comment to delete
    comment = dao.insert(id_user, id_movie, "To delete")

    # Delete the comment
    dao.delete(comment)

    # Ensure the comment is deleted
    comments = dao.get_user_comment(id_user, id_movie)
    assert len(comments) == 0
