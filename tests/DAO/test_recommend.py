import unittest
from datetime import date
from typing import List
from unittest.mock import MagicMock

from src.DAO.db_connection import DBConnector
from src.DAO.recommend import Recommend
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser
from src.Model.genre import Genre
from src.Model.movie import Movie


class TestRecommend(unittest.TestCase):

    def setUp(self):
        # Mock the DB connection and UserDao
        self.mock_db_connection = MagicMock(spec=DBConnector)
        self.mock_user_dao = MagicMock(spec=UserDao)
        self.mock_recommend = MagicMock(spec=Recommend)

        # Create the Recommend instance with the mocked DB connection
        self.recommend = Recommend(self.mock_db_connection)

        # Mock data
        self.mock_movies = [
            Movie(
                id_movie=1,
                title="Movie 1",
                belongs_to_collection=None,
                budget=1000000,
                genres=[Genre(id=123, name="Musical Comedy")],
                origin_country=["US"],
                original_language="en",
                original_title="Movie 1",
                overview="Overview 1",
                popularity=8.5,
                release_date=date(2023, 1, 1),
                revenue=5000000,
                runtime=120,
                vote_average=7.5,
                vote_count=1000,
                adult=False,
            ),
            Movie(
                id_movie=2,
                title="Movie 2",
                belongs_to_collection=None,
                budget=2000000,
                genres=[Genre(id=1, name="Comedy")],
                origin_country=["US"],
                original_language="en",
                original_title="Movie 2",
                overview="Overview 2",
                popularity=9.0,
                release_date=date(2023, 2, 1),
                revenue=6000000,
                runtime=110,
                vote_average=8.0,
                vote_count=1500,
                adult=False,
            ),
        ]

        self.mock_users = [
            ConnectedUser(
                id_user=1,
                username="user1",
                hashed_password="hashed1",
                date_of_birth=date(1990, 1, 1),
                gender=1,
                first_name="First1",
                last_name="Last1",
                email_address="user1@example.com",
                password_token="token1",
                phone_number="1234567890",
                own_film_collection=[1],
                follow_list=[2],
            ),
            ConnectedUser(
                id_user=2,
                username="user2",
                hashed_password="hashed2",
                date_of_birth=date(1992, 2, 2),
                gender=2,
                first_name="First2",
                last_name="Last2",
                email_address="user2@example.com",
                password_token="token2",
                phone_number="0987654321",
                own_film_collection=[2],
                follow_list=[1],
            ),
        ]

    def test_recommend_movies(self):
        # Mock the SQL query result
        self.mock_db_connection.sql_query.return_value = [
            {
                "id_movie": 2,
                "title": "Movie 2",
                "belongs_to_collection": None,
                "budget": 2000000,
                "genres": ["Comedy"],
                "origin_country": ["US"],
                "original_language": "en",
                "original_title": "Movie 2",
                "overview": "Overview 2",
                "popularity": 9.0,
                "release_date": date(2023, 2, 1),
                "revenue": 6000000,
                "runtime": 110,
                "vote_average": 8.0,
                "vote_count": 1500,
                "adult": False,
            }
        ]

        recommended_movies = self.recommend.recommend_movies(1)
        self.assertEqual(len(recommended_movies), 1)
        # self.assertEqual(recommended_movies[0]["id_movie"], 2)

    def test_recommend_users_to_follow(self):
        # Mock the SQL query result
        self.mock_db_connection.sql_query.return_value = [
            {
                "id_user": 2,
                "username": "user2",
                "hashed_password": "hashed2",
                "date_of_birth": date(1992, 2, 2),
                "gender": 2,
                "first_name": "First2",
                "last_name": "Last2",
                "email_address": "user2@example.com",
                "password_token": "token2",
                "phone_number": "0987654321",
                "own_film_collection": [2],
                "follow_list": [1],
            }
        ]  # [{"id_user": 2, "mutual": 1}]
        # Mock the user retrieval
        self.mock_user_dao.get_user_by_id.return_value = self.mock_users[1]

        recommended_users = self.recommend.recommend_users_to_follow(1)
        self.assertEqual(len(recommended_users), 1)
        self.assertEqual(recommended_users[0].id_user, 2)


if __name__ == "__main__":
    unittest.main()
