from typing import List

from src.DAO.db_connection import DBConnector
from src.Model.connected_user import ConnectedUser


class UserDao(metaclass=Singleton):
    """
    User DAO..
    """

    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def insert(self,new_user) -> ConnectedUser | None:
        """insert a Connected User into the database"""
        try : 
        # User already exists
        query = """
                SELECT COUNT(*)
                FROM users
                WHERE id_user = %s;
            """
        result = result = self.db_connection.sql_query(query, (new_user.id_user))
        user_exist = result["count"] > 0  # True si film, False sinon

        if not user_exist:
            print(f"Inserting User : {new_user.username}")
            insert_query = """
                        INSERT INTO users (id_user, username, hashed_password,
                                        date_of_birth, gender, first_name, last_name,
                                        email_address, token, phone_number) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values= (
                new_user.id_user,
                new_user.username,
                new_user.hashed_password,
                new_user.date_of_birth,
                new_user.gender,
                new_user.first_name,
                new_user.last_name,
                new_user.email_address,
                new_user.token,
                (
                    new_user.phone_number
                    if new_user.phone_number is not None
                    else None
                ),
            )
            self.db_connection.sql_query(insert_query, values )
            print(f"Insertion user successful: {new_user.username}")

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
            user = dict(result)
            return ConnectedUser(**user)  # Crée et retourne l'utilisateur connecté
        else:
            return None  # Aucun utilisateur trouvé


    def get_user_by_name(self, search_string, size=10) -> List[ConnectedUser]:
        """
        Fetch some users by their name
        """
        search_string = str(search_string).lower()
        try:
            query = "SELECT * FROM users WHERE LOWER(username) LIKE %s OR LOWER(last_name) LIKE %s OR LOWER(first_name) LIKE %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            "%" + search_string + "%",
                            "%" + search_string + "%",
                            "%" + search_string + "%",
                        ),
                    )
                    results = cursor.fetchmany(size)
        except Exception as e:
            print(f"Error while searching: {e}")
            return None
        if results:
            users_read = [ConnectedUser(**res) for res in results]
            return users_read
        return None

    # READ (Fetch all users)
    def get_all_users(self, limit: int = 10, offset: int = 0) -> List[ConnectedUser]:
        try:
            query = f"SELECT * FROM users LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, ())
                    results = cursor.fetchall()
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
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (email_address,))
                    results = cursor.fetchone()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        if results:
            print(f"{email_address} already exist in our database")
            return None
        else:
            return 1

    # check username
    def check_username(self, username: str):
        try:
            query = f"SELECT * FROM users WHERE username = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (username,))
                    results = cursor.fetchone()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        if results:
            print(f"{username} already exist in our database")
            return None
        else:
            return 1

    # UPDATE
    def update_user(
        self,
        id_user: int,
        username: str = None,
        hashed_password: str = None,
        date_of_birth: str = None,
        gender: int = None,
        first_name: str = None,
        last_name: str = None,
        email_address: str = None,
        phone_number: str = None,
    ):
        try:
            # Build the dynamic query based on the provided parameters
            updates = []
            values = []

            if username:
                updates.append("username = %s")
                values.append(username)
            if email_address:
                updates.append("email_address = %s")
                values.append(email_address)
            if hashed_password:
                updates.append("hashed_password = %s")
                values.append(hashed_password)
            if phone_number:
                updates.append("phone_number = %s")
                values.append(phone_number)
            if date_of_birth:
                updates.append("date_of_birth = %s")
                values.append(date_of_birth)
            if gender:
                updates.append("gender = %s")
                values.append(gender)
            if first_name:
                updates.append("first_name = %s")
                values.append(first_name)
            if last_name:
                updates.append("last_name = %s")
                values.append(last_name)

            # If there are no updates, return
            if not updates:
                print("No data provided for update.")
                return None

            query = f"UPDATE users SET {', '.join(updates)} WHERE id_user = %s"
            values.append(id_user)
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    connection.commit()
            print(f"User {id_user} updated successfully!")
            return 1

        except Exception as e:
            print(f"Error updating user: {e}")
            self.db_connection.connection.rollback()
            return None

    # DELETE
    def delete_user(self, id_user):
        try:
            query = "DELETE FROM users WHERE id_user = %s"
            with self.db_connection.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_user,),
                    )
                    connection.commit()
                    print("Record deleted successfully FROM users.")
        except Exception as e:
            print(f"Error while deleting FROM users: {e}")
            self.db_connection.connection.rollback()
            return None
