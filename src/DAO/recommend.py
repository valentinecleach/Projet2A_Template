from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
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
        Recommend movies to a user based on their own film collection.

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
            WITH PotentialMovies AS (
                SELECT m.id_movie, m.popularity, m.vote_average, l.id_genre
                FROM movie m
                JOIN link_movie_genre l USING(id_genre)
                WHERE m.id_movie NOT IN (
                    SELECT id_movie 
                    FROM user_movie_collection 
                    WHERE id_user = %s
                )
            ),
            UserGenreCounts AS (
                SELECT l.id_genre, COUNT(*) AS genre_count
                FROM user_movie_collection c
                JOIN link_movie_genre l USING(id_movie)
                WHERE c.id_user = %s
                GROUP BY l.id_genre
            )
            SELECT p.id_movie, SUM(u.genre_count) AS score, p.popularity, p.vote_average
            FROM PotentialMovies p
            RIGHT JOIN UserGenreCounts u ON p.id_genre = u.id_genre
            GROUP BY p.id_movie, p.popularity, p.vote_average
            ORDER BY score DESC, p.popularity DESC, p.vote_average DESC
            LIMIT 50;
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
            movie_dao = MovieDAO(self.db_connection)
            movies_read = [movie_dao.get_by_id(mov["id_movie"]) for mov in results]
            return movies_read
        else:
            return None

    def recommend_users_to_follow(self, id_user: int) -> List[ConnectedUser]:
        """
        Recommend users to follow based on mutual interests and connections based on their movie collection.

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
            --find users and count their movies
            WITH UserMovies AS (
            SELECT id_user, count(*) as nbmovies
            FROM user_movie_collection
            GROUP BY id_user
            ),
            --find users with mutual movies
            WITH MutualMovies AS (
            SELECT c2.id_user, nbmovies, COUNT(*) as mutual
            FROM user_movie_collection c1
            JOIN user_movie_collection c2 USING(id_movie)
            INNER JOIN UserMovies u ON u.id_user = c2.id_user
            WHERE c1.id_user = %s AND c2.id_user <> %s
            GROUP BY c2.id_user
            ),
            GenreFrequencies AS (
                SELECT c.id_user, l.id_genre, COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (PARTITION BY c.id_user) as frequency
                FROM user_movie_collection c
                JOIN link_movie_genre l USING(id_movie)
                GROUP BY c.id_user, l.id_genre
            ),
            UserGenreFrequencies AS (
                SELECT l.id_genre, COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () as frequency_user
                FROM user_movie_collection c
                JOIN link_movie_genre l USING(id_movie)
                WHERE c.id_user = %s
                GROUP BY l.id_genre
            ),
            MutualGenres AS (
                SELECT g1.id_user, SUM(g1.frequency * g2.frequency_user) as Mutual_genre
                FROM GenreFrequencies g1
                JOIN UserGenreFrequencies g2 USING(id_genre)
                GROUP BY g1.id_user
            )
            SELECT Mu.id_user as id_user,Mg.Mutual_genre, Mu.mutual/Mu.nbmovies as similar
            FROM MutualGenres Mg
            RIGHT JOIN  MutualMovies Mu ON Mu.id_user = Mg.id_user
            ORDER BY Mg.Mutual_genre DESC,similar DESC
            LIMIT 50;

            """
            results = self.db_connection.sql_query(
                query,
                (
                    id_user,
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
