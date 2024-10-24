from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnection, Singleton
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.Model.comment import Comment


class CommentDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnection):
        # create a DB connection object
        self.db_connection = db_connection
        # Create tables if don't exist
        self.db_connection.create_tables()

    # CREATE
    def insert(self, id_user: int, id_movie: int, comment: str):
        date = datetime.now()
        if comment:
            values = (id_user, id_movie, comment, date)
            try:
                with self.db_connection.connection.cursor() as cursor:
                    query = "INSERT INTO comment(id_user, id_movie, comment, date) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, values)
                    self.db_connection.connection.commit()

                user = UserDao().get_user_by_id(id_user)
                movie = MovieDAO().get_by_id(id_movie)
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
            query = "SELECT * FROM  comment" "WHERE id_user = %s and id_movie = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user, id_movie))
                    results = cursor.fetchall()
            if results:
                user = UserDao().get_user_by_id(id_user)
                movie = MovieDAO().get_by_id(id_movie)
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
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_movie))
                    results = cursor.fetchall()
            if results:
                movie = MovieDAO().get_by_id(id_movie)
                com = [
                    Comment(
                        user=UserDao().get_user_by_id(res["id_user"]),
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
        id_user = com.id_user
        id_movie = com.id_movie
        date = com.date
        try:
            query = "DELETE FROM  comment WHERE id_user = %s and id_movie = %s and date = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_movie,
                            date,
                        ),
                    )
                    connection.commit()
                    print("Record deleted successfully from comments.")
        except Exception as e:
            print(f"Error while deleting from comments: {e}")
            return None

    def get_overall(id_movie: int):
        try:
            query = "SELECT COUNT(*) as number FROM  comment WHERE id_movie = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_movie,),
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Error while averaging comments of movie {id_movie}: {e}")
            return None
        if res:
            return res["number"]
