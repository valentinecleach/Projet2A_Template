from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao

# Model
from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class Recommend:

    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def recommend_movies(self, id_user: int) -> List[Movie]:
        """
        Recommend movies to a user based on their own film collection and movie popularity.

        Parameters:
        -----------
        id_user : int
            The user to whom we are recommending movies.

        Returns:
        --------
        List[Movie]
            A list of recommended movies.
        """
        try:
            query = """
                SELECT * FROM movie
                WHERE id_movie not in (
                select id_movie from user_movie_collection
                where id_user = %s)
                ORDER BY popularity DESC, vote_average DESC
                LIMIT 20
            """
            results = self.db_connection.sql_query(query, (id_user,), return_type="all")
        except Exception as e:
            print(f"Error while searching: {e}")
            return None

        if results:
            movies_read = [Movie(**dict(mov)).to_dict() for mov in results]
            return movies_read
        else:
            return None

    def recommend_users_to_follow(self, id_user: int) -> List[ConnectedUser]:
        """
        Recommend users to follow based on mutual interests and connections.

        Parameters:
        -----------
        id_user : int
            The user to whom we are recommending other users to follow.
        Returns:
        --------
        List[ConnectedUser]
            A list of recommended users to follow.

        """
        # Sort users by the number of mutual films in their collections
        try:
            query = """
                SELECT c2.id_user as id_user, COUNT(*) as similitude
                FROM user_movie_collection c1
                JOIN user_movie_collection c2 using(id_movie)
                WHERE c1.id_user = %s and c2.id_user <> %s
                GROUP BY c2.id_user
                ORDER BY similitude DESC
                LIMIT 20
                """
            results = self.db_connection.sql_query(
                query,
                (
                    id_user,
                    id_user,
                ),
                return_type="all",
            )

        except Exception as e:
            print(f"Error while searching: {e}")
            return None

        if results:
            user_dao = UserDao(self.db_connection)
            users_read = [user_dao.get_user_by_id(res["id_user"]) for res in results]
            return users_read
        else:
            return None
