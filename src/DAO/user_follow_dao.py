from datetime import datetime
from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.connected_user import ConnectedUser


class UserFollowDao(metaclass=Singleton):
    """UserFollowDao is DAO for managing a who users follow in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    """
    
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        if not isinstance(db_connection, DBConnector):
            raise ValueError("db_connection must be an instance of DBConnector")
        self.db_connection = db_connection

    def insert(self, id_user: int, id_user_followed: int):
        """Inserts a follow relationship between users if it doesn't already exist.
        
        Parameters
        ----------
        id_user : int
            The ID of a user who wants a follow relationship
        id_user_followed : int
            The ID of a user who wants a follow relationship
        """
        try:
            # Verifying the existence of the relationship
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
        self, id_user: int
    ) -> list|None:
        """Gets all users followed by a specific user with pagination.

        Parameters
        ----------
        id_user : int
            The ID of the user who we want to know their list of users they follow.

        Returns
        -------
        list[int] | none
            The list of IDs of users followed. 
            If none can bne found, the method returns None
        """
        try:
            query = """
                SELECT * FROM follower
                WHERE id_user = %s;
            """
            results = self.db_connection.sql_query(
                query, (id_user,), return_type="all"
            )
            if results:
                follow_list = [result['id_user_followed'] for result in results]
                return follow_list
            else:
                return None
        except Exception as e:
            print(f"Error while fetching from follower: {e}")
            return None

    def delete(self, id_user: int, id_user_followed: int):
        """Deletes a follow relationship between two users.
        
        Parameters
        ----------
        id_user : int
            The ID of a user  
        id_user_followed : int
            The ID of a user 
        """
        try:
            query = """
            DELETE FROM follower WHERE id_user = %s AND id_user_followed = %s
            """
            self.db_connection.sql_query(query, (id_user, id_user_followed))
            print("Record deleted successfully from follower.")
        except Exception as e:
            print(f"Error while deleting from follower: {e}")

    def is_following(self, id_user: int, id_user_followed: int) -> bool:
        """Checks if a follow relationship exists between two users.
        
        Parameters
        ----------
        id_user : int
            The ID of a user.
        id_user_followed : int
            The ID of a user.

        Returns
        -------
        bool
            True if the users are following each other, false if else.
        """
        try:
            query = """
                SELECT COUNT(*) as count FROM follower
                WHERE id_user= %s AND id_user_followed = %s;
            """
            result = self.db_connection.sql_query(
                query, (id_user, id_user_followed), return_type="one"
            )
            return result["count"] > 0 if result else False
        except Exception as e:
            print(f"Error while checking follow relationship: {e}")
            return False
