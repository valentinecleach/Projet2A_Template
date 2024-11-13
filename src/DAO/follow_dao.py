from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.tables_creation import TablesCreation
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class FollowDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    # CREATE
    def insert(self, id_user: int, id_user_followed: int):
        date = datetime.now()
        values = (id_user, id_user_followed, date)
        try:
            with self.db_connection.connection.cursor() as cursor:
                query = f"INSERT INTO follower(id_user, id_user_followed,date) VALUES ({', '.join(['%s'] * len(values))})"
                res = cursor.execute(query, values)
                self.db_connection.connection.commit()

        except Exception as e:
            print(f"Erreur lors de l'insertion dans follower: {str(e)}")
            self.db_connection.connection.rollback()
            return None
        if res:
            return res

    # READ (Fetch all follower)
    def get_follow_list(self, id_user: int) -> List[ConnectedUser]:

        try:
            query = "SELECT * FROM follower WHERE id_user = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching from {table}: {e}")
            return None
        if results:
            id_read = [res["id_followed"] for res in results]
            users = [UserDao(self.db_connection).get_user_by_id(id) for id in id_read]
        return users

    # DELETE
    def delete_followed(self, id_user: int, id_user_followed: int):
        try:
            query = "DELETE FROM  follower WHERE id_user = %s and id_user_followed = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_user_followed,
                        ),
                    )
                    connection.commit()
                    print("Record deleted successfully from follower.")
        except Exception as e:
            print(f"Error while deleting from follower: {e}")
            return None
