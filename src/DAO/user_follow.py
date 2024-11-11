from src.DAO.db_connection import DBConnector
from src.Dao.user_dao import UserDao
from src.Model.connected_user import ConnectedUser


class UserFollowDAO:
    def __init__(self, db_connection: DBConnector):
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
                (
                    id_user,
                    id_user_followed,
                ),
                return_type="one",
            )

            # Vérifiez si la relation existe
            follow_exists = result["count"] > 0 if result else False

            if not follow_exists:
                print("Inserting follow relationship.")
                insert_query = """
                    INSERT INTO follower (id_user, id_user_followed)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(
                    insert_query,
                    (
                        id_user,
                        id_user_followed,
                    ),
                )
                print("Insertion successful: Follow relationship added.")
            else:
                print("Follow relationship already exists, no insertion performed.")

        except Exception as e:
            print("Insertion error: ", str(e))

    def get_all_user_followed(
        self, id_user: int, limit: int = 10, offset: int = 0
    ) -> list[connectedUser]:
        try:
            query = f"SELECT * FROM follower WHERE id_user = %s LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching FROM follower: {e}")
            return None
        if results:
            user_dao = UserDao(db_connection)
            return [user_dao.get_user_by_id(**res) for res in results]

    def delete(self, id_user: int, id_user_followed: int):
        try:
            query = "DELETE FROM follower WHERE id_user = %s and id_user_followed = %s"
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
                    print("Record deleted successfully FROM follower.")
        except Exception as e:
            print(f"Error while deleting FROM follower: {e}")
            self.db_connection.connection.rollback()
            return None
