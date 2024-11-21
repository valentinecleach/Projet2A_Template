from typing import Dict, List

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.connected_user import ConnectedUser
from src.DAO.user_favorites_dao import UserFavoriteDao
from src.DAO.user_follow_dao import UserFollowDao

class UserDao(metaclass=Singleton):
    """
    User DAO..
    """

    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection
        self.user_favorites_dao = UserFavoriteDao(db_connection)
        self.user_follow_dao = UserFollowDao(db_connection)

    def insert(self, new_user: Dict) -> ConnectedUser | None:
        """insert a Connected User into the database"""
        try:
            # User already exists
            query = """
                    SELECT COUNT(*)
                    FROM users
                    WHERE username = %s;
                """
            result = result = self.db_connection.sql_query(
                query, (new_user["username"],)
            )
            user_exist = result["count"] > 0  # True si film, False sinon

            if not user_exist:
                print(f"Inserting User : {new_user['username']}")
                insert_query = """
                            INSERT INTO users (username, hashed_password,
                                            date_of_birth, gender, first_name, last_name,
                                            email_address, phone_number, password_token) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                self.db_connection.sql_query(insert_query, values)
                print(f"Insertion user successful: {new_user['username']}")
        except Exception as e:
            print(f"Insertion error: {str(e)}")

    def get_user_by_id(self, id_user: int) -> ConnectedUser | None:
        """Fetches a single user by its ID."""
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
            user.update({'own_film_collection' : own_film_collection , 'follow_list' : follow_list })
            return ConnectedUser(**user)  # Crée et retourne l'utilisateur connecté
        else:
            return None  # Aucun utilisateur trouvé

    def get_user_by_name(self, username: str) -> List[ConnectedUser]:
        """
        Fetch some users by their name
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
                users_read = [self.get_user_by_id(user['id_user']) for user in results]  # .to_dict()
                return users_read
            else:
                return None
        except Exception as e:
            print(f"Error while searching: {e}")
            return None



    # READ (Fetch all users)
    def get_all_users(self, limit: int = 10, offset: int = 0) -> List[ConnectedUser]:
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
    def check_email_address(self, email_address: str):
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
    def update_user(
        self,
        connected_user : ConnectedUser
    ):
        """ 
        Allow the user to update his email_adress or his phone number
        """
        try:
            if self.check_email_address(connected_user.email_address):
                update_query = """
                    UPDATE users
                    SET email_address = %s, phone_number = %s
                    WHERE id_user = %s;
                """
                values = (connected_user.email_address, connected_user.phone_number, connected_user.id_user)
                self.db_connection.sql_query(update_query, values)
                print(f"Update successful for user {connected_user.username}")
        except Exception as e:
            print("Update error:", str(e))

    # DELETE
    def delete_user(self, id_user):
        try:
            query = "DELETE FROM users WHERE id_user = %s"
            self.db_connection.sql_query(query, (id_user,))
            print(f"The user with id {id_user} was succesfully deleted.")
        except Exception as e:
            print(f"Error while deleting FROM users: {e}")
            return None


# db_connection = DBConnector()
# my_object = UserDao(db_connection)
# print(my_object.get_user_by_name('garrettmercer'))
# #print(my_object.get_user_by_id(217))
