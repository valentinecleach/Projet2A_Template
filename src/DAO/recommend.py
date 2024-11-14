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
                SELECT tab.id_movie as id_movie, SUM(frequency_user) as score,
                        popularity , vote_average
                FROM
                    (SELECT m.id_movie as id_movie,popularity, vote_average , id_genre
                    FROM movie m JOIN link_movie_genre l using(id_genre)
                    WHERE m.id_movie not in (
                    select id_movie from user_movie_collection c
                    where id_user = %s) as tab

                    JOIN 

                    (SELECT tab4.id_genre as id_genre, 
                                    genre_count/total_genre as frequency_user
                                FROM
                                    (SELECT l3.id_genre as id_genre, 
                                        COUNT(*) AS genre_count
                                    From user_movie_collection c3
                                            JOIN link_movie_genre l3 using(id_movie)
                                        Where c3.id_user = %s
                                        Group BY l3.id_genre
                                    ) as tab4
                    USING(id_genre)
                GROUP BY id_movie
                ORDER BY score DESC, popularity DESC, vote_average DESC
            """
            results = self.db_connection.sql_query(query, (id_user,), return_type="all")
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
            SELECT Mu.id_user as id_user
            FROM
                (SELECT c2.id_user as id_user, COUNT(*) as mutual
                FROM user_movie_collection c1
                JOIN user_movie_collection c2 using(id_movie)
                WHERE c1.id_user = %s and c2.id_user <> %s
                GROUP BY c2.id_user) as Mu

                FULL JOIN 

                (SELECT tab3.id_user as id_user, 
                        SUM(tab3.frequency * tab5.frequency_user) as Mutual_genre
                FROM
                       (SELECT tab1.id_user as id_user,
                            tab1.id_genre as id_genre, 
                            genre_count/total_genre as frequency
                        FROM
                            
                            (SELECT c.id_user as id_user,
                                l.id_genre as id_genre, 
                                COUNT(*) AS genre_countdb
                            From user_movie_collection c
                                    JOIN link_movie_genre l using(id_movie)
                                Group BY c.id_user, l.id_genre
                            ) as tab1
                            INNER JOIN
                                (SELECT C2.id_user as id_user, COUNT(*) as total_genre
                                From user_movie_collection c2
                                JOIN link_movie_genre l2 using(id_movie)
                                GROUP BY C2.id_user
                                ) AS tab2
                            ON tab1.id_genre = tab2.id_genre
                        )AS tab3
                        JOIN
                            (SELECT tab4.id_genre as id_genre, 
                                genre_count/total_genre as frequency_user
                            FROM
                                (SELECT l3.id_genre as id_genre, 
                                    COUNT(*) AS genre_count
                                From user_movie_collection c3
                                        JOIN link_movie_genre l3 using(id_movie)
                                    Where c3.id_user = %s
                                    Group BY l3.id_genre
                                ) as tab4
                                INNER JOIN
                                    (SELECT COUNT(*) as total_genre
                                    From user_movie_collection c4
                                    JOIN link_movie_genre l4 using(id_movie)
                                    Where c4.id_user = %s
                                    ) AS tab5
                                ON tab4.id_genre = tab5.id_genre
                            )AS tab6
                        Using(id_genre)
                Group by tab3.id_user
                ) as ge
                ON ge.id_user = Mu.id_user
            ORDER BY mutual DESC, Mutual_genre DESC
                

                """
            results = self.db_connection.sql_query(
                query,
                (
                    id_user,
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
