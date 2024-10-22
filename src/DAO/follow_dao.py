from datetime import datetime
from typing import List  # , Optional

from src.DAO.db_connection import DBConnection, Singleton
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class FollowDao(metaclass=Singleton):
    # CREATE
    def insert(self, id_user: int, id_user_followed: int):
        date = datetime.now()
        values = (id_user, id_user_followed, date)
        try:
            with DBConnection().connection.cursor() as cursor:
                query = f"INSERT INTO follower(id_user, id_user_followed,date) VALUES ({', '.join(['%s'] * len(values))})"
                res = cursor.execute(query, values)
                DBConnection().connection.commit()
                
        except Exception as e:
            print(f"Erreur lors de l'insertion dans follower: {str(e)}")
            DBConnection().connection.rollback()
            return None 
        if res:
            return res

    # READ (Fetch all follower)
    def get_follow_list(self, id_user: int) -> List[ConnectedUser]:

        try:
            query = "SELECT * FROM follower WHERE id_user = %s"
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching from {table}: {e}")
            return None
        if results:
            id_read = [res["id_followed"] for res in results]
            users = [UserDao().get_user_by_id(id) for id in id_read]
        return users

    # DELETE
    def delete_followed(self, id_user: int, id_user_followed: int):
        try:
            query = (
                "DELETE FROM  follower WHERE id_user = %s and id_user_followed = %s"
            )
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            id_user,
                            id_user_followed,
                        ),
                    )
                    connection.commit()
                    print(f"Record deleted successfully from follower.")
        except Exception as e:
            print(f"Error while deleting from follower: {e}")
            return None
