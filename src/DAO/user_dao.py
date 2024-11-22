from typing import Dict, List, Union

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.user_favorites_dao import UserFavoriteDao
from src.DAO.user_follow_dao import UserFollowDao
from src.Model.connected_user import ConnectedUser


class UserDao(metaclass=Singleton):
    """UserDao is DAO for managing users in the database.

    Attributes
    ----------
    db_connection : DBConnector
        A connector to the database.
    user_favorites_dao : UserFavoriteDao
        A DAO a users favorite movies
    user_follow_dao : UserFollowDao
        A DAO of the users that a user follows
    """

    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_favorites_dao = UserFavoriteDao(db_connection)
        self.user_follow_dao = UserFollowDao(db_connection)

    def insert(self, new_user: Dict):
        """Inserts a Connected User into the database

        Parameters
        ----------
        new_user : Dict
            A new user to add to the database
        """
        try:
            # If user already exists
            query = """
                    SELECT COUNT(*)
                    FROM users
                    WHERE username = %s;
                """
            result = result = self.db_connection.sql_query(
                query, (new_user["username"],), return_type="one"
            )
            user_exist = result["count"] > 0  # True if film b but False otherwise

            if not user_exist:
                print(f"Inserting User : {new_user['username']}")
                insert_query = """
                            INSERT INTO users (username, hashed_password,
                                            date_of_birth, gender, first_name, last_name,
                                            email_address, phone_number, password_token) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id_user;
                """
                values = (
                    new_user["username"],
                    new_user["hashed_password"],
                    new_user["date_of_birth"],
                    new_user["gender"],
                    new_user["first_name"],
                    new_user["last_name"],
                    new_user["email_address"],
                    (
                        new_user["phone_number"]
                        if new_user["phone_number"] is not None
                        else None
                    ),
                    new_user["password_token"],
                )
                result = self.db_connection.sql_query(
                    insert_query, values, return_type="one"
                )
                if result:
                    id_user = result["id_user"]
                    new_user.update({"id_user": id_user})
                    print(
                        f"Insertion user successful: {new_user['username']}, with id : {result['id_user']}"
                    )
                    return ConnectedUser(**new_user)
        except Exception as e:
            print(f"Insertion error: {str(e)}")

    def get_user_by_id(self, id_user: int) -> ConnectedUser | None:
        """Fetches a single user by its ID.

        Parameters
        ----------
        id_user : int
            The ID of a user to fetch

        Returns
        -------
        ConnectedUser | None
            The user that is fetched. If the ID doesn't correspond to a user, the method returns None
        """
        try:
            query = "SELECT * FROM users WHERE id_user = %s"
            result = self.db_connection.sql_query(query, (id_user,), return_type="one")
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        if result:
            own_film_collection = self.user_favorites_dao.get_favorites(id_user)
            follow_list = self.user_follow_dao.get_all_user_followed(id_user)
            user = dict(result)
            user.update(
                {"own_film_collection": own_film_collection, "follow_list": follow_list}
            )
            return ConnectedUser(**user)  # Creates and returns a connected user
        else:
            return None  # No user found

    def get_user_by_name(self, username: str) -> List[ConnectedUser]:
        """Fetches users by their name.

        Parameters
        ----------
        username : str
            The username of a user to look for.

        Returns
        -------
        List[ConnectedUser] | None
            A list of users with the username. If no users are found, the method returns None.
        """
        try:
            query = """
                SELECT id_user FROM users 
                WHERE username LIKE %s 
            """
            search_pattern = "%" + username + "%"
            results = self.db_connection.sql_query(
                query, (search_pattern,), return_type="all"
            )
            if results:
                users_read = [
                    self.get_user_by_id(user["id_user"]) for user in results
                ]  # .to_dict()
                return users_read
            else:
                return None
        except Exception as e:
            print(f"Error while searching: {e}")
            return None

    def get_all_users(
        self, limit: int = 10, offset: int = 0
    ) -> List[ConnectedUser] | None:
        """Fetches all users within a limit

        Parameters
        ----------
        limit : int = 10
            The maximum of users to return
        offset : int = 0
            The ??

        Returns
        List[ConnectedUser] | None
            Returns a list of users. If no users are found, it returns None.
        """
        try:
            query = f"SELECT * FROM users LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            results = self.db_connection.sql_query(query, (), return_type="all")
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        if results:
            users_read = [ConnectedUser(**res) for res in results]
            return users_read
        return None

    # check email_address, username
    def check_email_address(self, email_address: str) -> Union[bool, None]:
        """Checks if an email adress is associated to a user in the database.

        Parameters
        ----------
        email_address : str
            The email_address to check

        Returns
        -------
        True | None
            If the email_adress is associated to a user, the method returns True.
            If not, it returns None.
        """
        try:
            query = f"SELECT * FROM users WHERE email_address = %s"
            results = self.db_connection.sql_query(
                query, (email_address,), return_type="one"
            )
            if results:
                print(f"{email_address} already exist in our database")
                return None
            else:
                return True
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None

    # UPDATE
    def update_user(self, connected_user: ConnectedUser, is_new_mail: bool):
        """Allows a user to update their email_adress.

        Parameters
        ----------
        connected_user : ConnectedUser
            The user that wants to update their email adress.

        is_new_mail : bool -> pas un pb ca?

        """
        try:
            if is_new_mail:
                self.check_email_address(connected_user.email_address)
            update_query = """
                UPDATE users
                SET email_address = %s, phone_number = %s
                WHERE id_user = %s;
            """
            values = (
                connected_user.email_address,
                connected_user.phone_number,
                connected_user.id_user,
            )
            self.db_connection.sql_query(update_query, values)
            print(f"Update successful for user {connected_user.username}")
        except Exception as e:
            print("Update error:", str(e))

    def delete_user(self, id_user: int):
        """Deletes a user from the database

        Parameters
        ----------
        id_user : int
            The ID of the user that wants their account deleted.

        """
        try:
            query = "DELETE FROM users WHERE id_user = %s"
            self.db_connection.sql_query(query, (id_user,))
            print(f"The user with id {id_user} was succesfully deleted.")
        except Exception as e:
            print(f"Error while deleting FROM users: {e}")
            return None
