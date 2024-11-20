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
        self.user_dao = UserDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)

    # CREATE

    def insert(self, comments: Comment):
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM comment
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (comment.user.id_user, comment.movie.id_movie),
                return_type="one",
            )
            comment_exist = result["count"] > 0 if result else False
            if not comment_exist:
                print(f"Inserting comment relationship between user : {comment.user.username} and movie {comment.movie.id_movie}")
                query = """
                    INSERT INTO comment (id_user, id_movie, comment, date)
                    VALUES (%s, %s, %s, %s);
                """
                values = (
                    comment.user.id_user,
                    comment.movie.id_movie,
                    comment.comment,
                    comment.date,
                )
                self.db_connection.sql_query(query, values)
                print(
                    f"Insertion successful: Comment relationship between {comment.user.username} and {comment.movie.title} added."
                )
            else:
                print(f"Comment relationship between {comment.user.username} and {comment.movie.title} already exist. Try an update")
        except Exception as e:
            print("Insertion error:", str(e))

    def update(self, comment : Comment):
        try:
            update_query = """
                UPDATE comment
                SET comment = %s, date = %s
                WHERE id_user = %s AND id_movie = %s;
            """
            values = (comment.comment, comment.date, comment.user.id_user, comment.movie.id_movie)
            self.db_connection.sql_query(update_query, values)
            print(f"Update successful: Comment for {comment.user.username} and {comment.movie.title} updated.")
        except Exception as e:
            print("Update error:", str(e))

    # READ (Fetch a specific user's comment)
    def get_comment(
        self,
        id_user: int,
        id_movie: int,
    ) -> Comment:
        try:
            query = "SELECT * FROM  comment WHERE id_user = %s and id_movie = %s"
            result = self.db_connection.sql_query(
                query, (id_user, id_movie), return_type="one"
            )
            if result:
                user = self.user_dao.get_user_by_id(id_user)
                movie = self.movie_dao.get_by_id(id_movie)
                if user and movie:
                    comment = Comment(
                            user=user, movie=movie, date=result["date"], comment=result["comment"]
                        )
                    return comment
            else:
                print(f" Error while fetching user or Movie (id_user={id_user}, id_movie={id_movie}).")
                return None
        except Exception as e:
            print(f"Error while fetching user comment: {e}")
            return []

    # READ (Fetch all comments of a specific movie)
    def get_recent_comments_for_a_movie(
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
                movie = self.movie_dao.get_by_id(id_movie)
                com = [
                    Comment(
                        user=self.user_dao.get_user_by_id(res["id_user"]),
                        movie=movie,
                        date=res["date"],
                        comment=res["comment"],
                    )
                    for res in results
                ]
                return com
            else:
                print(f" Error while fetching for Movie : {movie}.")
                return None
        except Exception:
            return None

    # DELETE
    def delete(self, comment: Comment):
        """
        to delete a comment
        """
        try:
            query = "DELETE FROM  comment WHERE id_user = %s and id_movie = %s and date = %s"
            values = (comment.user.id_user, comment.movie.id_movie)
            self.db_connection.sql_query(
                query,
                values)
        except Exception as e:
            print(f"Error while deleting from comments: {e}")
            return None

    # def get_overall(self, id_movie: int):
    #     """
    #     count how many comment for a movie
    #     """

    #     try:
    #         query = "SELECT COUNT(*) as number FROM  comment WHERE id_movie = %s"
    #         res = self.db_connection.sql_query(query, (id_movie,), return_type="one")
    #     except Exception as e:
    #         print(f"Error while averaging comments of movie {id_movie}: {e}")
    #         return None
    #     if res:
    #         return res["number"]


# db = DBConnector()
# dao = CommentDao(db)
# print(dao.get_recent_comments(250))
