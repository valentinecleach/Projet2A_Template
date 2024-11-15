from datetime import datetime
from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class UserFollowDao:
    def __init__(self, db_connection: DBConnector):
        if not isinstance(db_connection, DBConnector):
            raise ValueError("db_connection must be an instance of DBConnector")
        self.db_connection = db_connection

    def insert(self, id_user: int, id_user_followed: int):
        """Insert a follow relationship between users if it doesn't already exist."""
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM follower
                WHERE id_user= %s AND id_user_followed = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (id_user, id_user_followed),
                return_type="one",
            )

            follow_exists = result["count"] > 0 if result else False

            if not follow_exists:
                print("Inserting follow relationship.")
                insert_query = """
                    INSERT INTO follower (id_user, id_user_followed, date)
                    VALUES (%s, %s, %s);
                """
                the_date = datetime.now().date()
                values = (id_user, id_user_followed, the_date)
                self.db_connection.sql_query(insert_query, values)
                print("Insertion successful: Follow relationship added.")
            else:
                print("Follow relationship already exists, no insertion performed.")
        except Exception as e:
            print("Insertion error:", str(e))

    def get_all_user_followed(
        self, id_user: int, limit: int = 10, offset: int = 0
    ) -> List[ConnectedUser]:
        """Get all users followed by a specific user with pagination."""
        try:
            query = """
                SELECT * FROM follower
                WHERE id_user = %s
                LIMIT %s OFFSET %s;
            """
            results = self.db_connection.sql_query(
                query, (id_user, max(0, limit), max(0, offset)), return_type="all"
            )
        except Exception as e:
            print(f"Error while fetching from follower: {e}")
            return None

        if results:
            user_dao = UserDao(self.db_connection)
            return [user_dao.get_user_by_id(res["id_user_followed"]) for res in results]
        return []

    def delete(self, id_user: int, id_user_followed: int):
        """Delete a follow relationship between two users."""
        try:
            query = "DELETE FROM follower WHERE id_user = %s AND id_user_followed = %s"
            self.db_connection.sql_query(query, (id_user, id_user_followed))
            print("Record deleted successfully from follower.")
        except Exception as e:
            print(f"Error while deleting from follower: {e}")

    def is_following(self, id_user: int, id_user_followed: int) -> bool:
        """Check if a follow relationship exists between two users."""
        try:
            query = """
                SELECT COUNT(*) as count FROM follower
                WHERE id_user = %s AND id_user_followed = %s;
            """
            result = self.db_connection.sql_query(
                query, (id_user, id_user_followed), return_type="one"
            )
            return result["count"] > 0 if result else False
        except Exception as e:
            print(f"Error while checking follow relationship: {e}")
            return False


# db_connection = DBConnector()
# my_object = UserFollowDAO(db_connection)
# #print(my_object.insert(1,2))  #works
# print(my_object.get_all_user_followed(1,2))
# #print(my_object.delete(1,2)) #works
# #print(my_object.is_following(1,2)) #works
