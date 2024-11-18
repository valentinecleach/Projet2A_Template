from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.singleton import Singleton
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment


class CommentDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    # CREATE

    def insert(self, id_user: int, id_movie: int, comment: str):
        try:
            user = UserDao(self.db_connection).get_user_by_id(id_user)
            movie = MovieDAO(self.db_connection).get_by_id(id_movie)
        except Exception as e:
            print(f"Erreur lors de la recherche du film: {str(e)}")
            return None
        date = datetime.now()
        if comment:
            values = (id_user, id_movie, comment, date)
            try:
                query = "INSERT INTO comment(id_user, id_movie, comment, date) VALUES (%s, %s, %s, %s)"
                self.db_connection.sql_query(query, values, return_type="one")
                return Comment(user=user, movie=movie, date=date, comment=comment)

            except Exception as e:
                print(f"Erreur lors de l'insertion dans comment: {str(e)}")
                self.db_connection.connection.rollback()
                return None

        return None

    # READ (Fetch a specific user's comment)
    def get_user_comment(
        self,
        id_user: int,
        id_movie: int,
    ) -> List[Comment]:

        try:
            query = "SELECT * FROM  comment WHERE id_user = %s and id_movie = %s"
            results = self.db_connection.sql_query(
                query, (id_user, id_movie), return_type="all"
            )
            if results:
                user = UserDao(self.db_connection).get_user_by_id(id_user)
                movie = MovieDAO(self.db_connection).get_by_id(id_movie)
                com = [
                    Comment(
                        user=user, movie=movie, date=res["date"], comment=res["comment"]
                    )
                    for res in results
                ]
                return com
            else:
                return []  # Liste vide si aucun commentaire n'est trouvé
        except Exception as e:
            print(f"Error while fetching user comment: {e}")
            return []

    # READ (Fetch all comments of a specific movie)
    def get_recent_comments(
        self,
        id_movie: int,
        limit: int = 10,
    ) -> List[Comment]:

        try:
            query = f"SELECT * FROM  comment WHERE id_movie = %s ORDER BY date DESC LIMIT {max(limit, 0)}"
            results = self.db_connection.sql_query(
                query, (id_movie,), return_type="all"
            )
            if results:
                movie = MovieDAO(self.db_connection).get_by_id(id_movie)
                com = [
                    Comment(
                        user=UserDao(self.db_connection).get_user_by_id(res["id_user"]),
                        movie=movie,
                        date=res["date"],
                        comment=res["comment"],
                    )
                    for res in results
                ]
                return com
            else:
                return None
        except Exception:
            return None

    # DELETE
    def delete(self, com: Comment):
        id_user = com.user.id_user
        id_movie = com.movie.id_movie
        date = com.date
        try:
            query = "DELETE FROM  comment WHERE id_user = %s and id_movie = %s and date = %s"
            self.db_connection.sql_query(
                query,
                (
                    id_user,
                    id_movie,
                    date,
                ),
            )
        except Exception as e:
            print(f"Error while deleting from comments: {e}")
            return None

    def get_overall(self, id_movie: int):
        try:
            query = "SELECT COUNT(*) as number FROM  comment WHERE id_movie = %s"
            res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
        except Exception as e:
            print(f"Error while averaging comments of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]


# db = DBConnector()
# dao = CommentDao(db)
# print(dao.get_recent_comments(250))
