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

        res = DBConnection().insert(cine.follower, values)

        return res

    # READ (Fetch all follower)
    def get_follow_list(self, id_user: int) -> List[ConnectedUser]:

        results = DBConnection().read_all_by_id(cine.follower, "id_user", id_user)
        if results:
            id_read = [res["id_followed"] for res in results]
            users = [UserDao().get_user_by_id(id) for id in id_read]
        return users

    # DELETE
    def delete_followed(self, id_user: int, id_user_followed: int):
        try:
            query = (
                "DELETE FROM cine.follower WHERE id_user = %s and id_user_followed = %s"
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
                    print("Record deleted successfully from follower.")
        except Exception as e:
            print(f"Error while deleting from follower: {e}")
            return None
