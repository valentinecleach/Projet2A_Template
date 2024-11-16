from datetime import date, datetime, timedelta
from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao

# Model
from src.Model.connected_user import ConnectedUser
from src.Model.movie import Movie


class RecommendDao:

    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def recommend_movies(self, id_user: int) -> List[Movie]:
        """
        Recommend movies to a user based on their own film collection, age, and gender.

        This algorithm recommends movies to a user by considering the following steps:
        1. **Collect User Information**:
        2. **Calculate Age Range around the user's date of birth to find users of similar age**:
        3. **Identify Potential Movies has not yet watched**:
        4. **Calculate Genre Frequencies of each movie genre in the collections of all users**:
        5. **Calculate the current user's Genre Frequencies**:
        6. **Calculate Genre Similarity**:
        7. **Combine Results**:
            - Combine the results from the genre similarity and age/gender analysis to recommend movies.

        Parameters:
        -----------
        id_user : int
            The user to whom we are recommending movies.

        Returns:
        --------
        List[Movie]
            A list of recommended movies.
        """
        # provide movies using his age and his gender

        try:
            dao = UserDao(self.db_connection)
            user = dao.get_user_by_id(id_user)
            gender = user.gender
            date_of_birth = user.date_of_birth

            updates = []
            values = []
            if gender:
                updates.append("gender = %s")
                values.append(gender)
            if date_of_birth:
                if isinstance(date_of_birth, str):
                    date_of_birth_obj = datetime.strptime(
                        date_of_birth, "%Y-%m-%d"
                    ).date()
                elif isinstance(date_of_birth, datetime):
                    date_of_birth_obj = date_of_birth.date()
                elif isinstance(date_of_birth, date):
                    date_of_birth_obj = date_of_birth
                else:
                    raise TypeError(
                        "date_of_birth must be a string, datetime, or date object"
                    )

                updates.append("date_of_birth BETWEEN %s AND %s")
                values.append(
                    (date_of_birth_obj - timedelta(days=3 * 365)).strftime("%Y-%m-%d")
                )
                values.append(
                    (date_of_birth_obj + timedelta(days=3 * 365)).strftime("%Y-%m-%d")
                )

            condition = (
                " AND ".join(updates) if updates else "1=1"
            )  # Default condition to avoid syntax error

        except (TypeError, ValueError) as e:
            print(f"Error while collecting date_of_birth and gender: {e}")
            return None

        try:
            query = f"""
            WITH PotentialMovies AS (
                SELECT m.id_movie, m.popularity, m.vote_average, l.id_genre
                FROM movie m
                JOIN link_movie_genre l USING(id_movie)
                WHERE m.id_movie NOT IN (
                    SELECT id_movie 
                    FROM user_movie_collection 
                    WHERE id_user = %s
                )ORDER BY popularity DESC, vote_average DESC
            ),
            UserGenreCounts AS (
                SELECT l.id_genre, COUNT(*) AS genre_count
                FROM user_movie_collection c
                JOIN link_movie_genre l USING(id_movie)
                WHERE c.id_user = %s
                GROUP BY l.id_genre
            ),
            AgeGender AS ( --movie popular in user's age and gender group
                SELECT m.id_movie, COUNT(*) AS Score
                FROM PotentialMovies m
                JOIN user_movie_collection c using(id_movie)
                JOIN users u USING(id_user)
                WHERE {condition}
                GROUP BY m.id_movie
                ORDER BY Score DESC
            ),
            Forward AS (--movie popular in user's social network
                SELECT c.id_movie
                FROM follower f1
                INNER JOIN follower f2 ON f1.id_user_followed = f2.id_user
                INNER JOIN user_movie_collection c 
                ON (c.id_user = f2.id_user_followed OR c.id_user = f2.id_user)
                WHERE f1.id_user = %s
            )
            SELECT DISTINCT id_movie
            FROM (
                (SELECT m.id_movie, COUNT(*) AS Score
                FROM PotentialMovies m
                JOIN Forward f using(id_movie)
                GROUP BY m.id_movie
                ORDER BY Score DESC
                LIMIT 5)
                UNION
                (SELECT id_movie, Score
                FROM AgeGender
                LIMIT 10)
                UNION
                (SELECT p.id_movie, SUM(u.genre_count) AS score
                FROM PotentialMovies p
                LEFT JOIN UserGenreCounts u ON p.id_genre = u.id_genre
                GROUP BY p.id_movie
                ORDER BY score DESC
                LIMIT 15)
            ) as f;
            """

            results = self.db_connection.sql_query(
                query,
                (id_user, id_user, *values, id_user),
                return_type="all",
            )
        except Exception as e:
            print(f"Error while searching: {e}")
            return None

        if results:
            movie_dao = MovieDAO(self.db_connection)
            movies_read = [movie_dao.get_by_id(mov["id_movie"]) for mov in results]
            return movies_read
        else:
            return None

    def recommend_users_to_follow(self, id_user: int) -> List[ConnectedUser]:
        """
        Recommend users to follow based on the user's movie genre preferences and their social network.

        This algorithm identifies potential users to follow by considering the following steps:
        1. **Identification of Potential Users**:
        2. **Calculation of Genre Frequencies all users**:
        3. **User's Genre Frequencies**:
        4. **Calculation of Genre Similarity**:
        5. **Identification of users who are followed by the friends of the current user**:
        6. **Combination of Results from the genre similarity and social network analysis to recommend users**:

        Parameters:
        -----------
        id_user : int
            The ID of the user for whom we are recommending other users to follow.

        Returns:
        --------
        List[ConnectedUser]
            A list of recommended users to follow.
        """

        # Sort users by the score of mutual films in their collections
        try:
            query = f"""
            WITH Potentialusers AS (
                SELECT id_user
                FROM users
                WHERE id_user NOT IN (
                    SELECT id_user_followed 
                    FROM follower
                    WHERE id_user = %s
                )
            ),
            -- find users and frequencies of their movies genre
            GenreFrequencies AS (
                SELECT c.id_user, l.id_genre, COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY c.id_user) AS frequency
                FROM user_movie_collection c
                JOIN link_movie_genre l USING(id_movie)
                GROUP BY c.id_user, l.id_genre
            ),
            -- find the user's frequencies of his movies genre
            UserGenreFrequencies AS (
                SELECT id_genre, frequency AS frequency_user
                FROM GenreFrequencies
                WHERE id_user = %s
            ),
            MutualGenres AS (
                SELECT g1.id_user, SUM(POWER((g1.frequency - g2.frequency_user),2)) AS Mutual_genre
                FROM GenreFrequencies g1
                JOIN UserGenreFrequencies g2 USING(id_genre)
                WHERE g1.id_user <> %s
                GROUP BY g1.id_user
            ),
            Forward AS (
                SELECT f2.id_user_followed AS follow, COUNT(*) AS Score
                FROM follower f1
                JOIN Potentialusers p USING(id_user)
                INNER JOIN follower f2 ON f1.id_user_followed = f2.id_user
                WHERE f1.id_user = %s
                GROUP BY f2.id_user_followed
            )
            SELECT DISTINCT id_user
            FROM (
                (SELECT id_user , Mg.Mutual_genre  as Score
                FROM MutualGenres Mg
                JOIN Potentialusers p USING(id_user)
                ORDER BY Mg.Mutual_genre ASC
                LIMIT 10)

                UNION

                (SELECT DISTINCT follow AS id_user,Score
                FROM (
                    (SELECT follow, Score
                    FROM Forward)
                    UNION
                    (SELECT f3.id_user_followed AS follow, COUNT(*) AS Score
                    FROM Forward f
                    INNER JOIN follower f3 ON f.follow = f3.id_user
                    GROUP BY f3.id_user_followed)
                ) AS tab
                ORDER BY Score DESC
                LIMIT 15)
            ) AS fin;
            """

            results = self.db_connection.sql_query(
                query,
                (id_user, id_user, id_user, id_user),
                return_type="all",
            )

        except Exception as e:
            print(f"Error while collecting: {e}")
            return None

        if results:
            user_dao = UserDao(self.db_connection)
            users_read = [user_dao.get_user_by_id(res["id_user"]) for res in results]
            return users_read
        else:
            return None

    def get_popular_movies(self) -> list[Movie]:
        """
        Description: Fetches the most popular movies based on their average rating and popularity.

        Returns:

        list[Movie]: List of the most popular movies.
        """
        try:
            query = """
                SELECT id_movie FROM Movie
                ORDER BY vote_average DESC, popularity DESC
                LIMIT 25
            """
            result = self.db_connection.sql_query(query, (), return_type="all")

        except Exception as e:
            print("Error during fetching movies:", str(e))
            return None
        if result:
            dao = MovieDAO(self.db_connection)
            return [dao.get_by_id(res["id_movie"]) for res in result]

    def get_popular_users(self, id_user) -> list[Movie]:
        """
        Description: Fetches the most popular users based on the number of followers, excluding the specified user.

        Parameters:
        -------------------------
        id_user (int): ID of the user to exclude.
        Returns:
        --------------------------
        list[User]: List of the most popular users.
        Does this work for you?




        """
        try:
            query = """
                SELECT id_user_followed , COUNT(*) as popularity
                FROM follower
                where id_user <> %s
                GROUP BY id_user_followed
                ORDER BY popularity DESC
                LIMIT 25
            """
            result = self.db_connection.sql_query(query, (id_user,), return_type="all")

        except Exception as e:
            print("Error during fetching popular users:", str(e))
            return None
        if result:
            user_dao = UserDao(self.db_connection)
            return [user_dao.get_user_by_id(res["id_user_followed"]) for res in result]


# db_connection = DBConnector()
# # u = UserDao(db_connection)
# dao = RecommendDao(db_connection)
# # #user = u.get_user_by_id(24)
# # # #print(user)
# # #print(dao.get_popular_users(24))
# dao.recommend_users_to_follow(24)
# print(len(dao.recommend_movies(24)))
# date_of_birth = user.date_of_birth
# print(isinstance(date_of_birth, date))
