from typing import List  # , Optional

from src.DAO.db_connection import DBConnection, Singleton
from src.Model.connected_user import ConnectedUser


class UserDao(metaclass=Singleton):
    # CREATE
    def insert(
        self,
        id_user: int,
        name: str,
        phone_number: str,
        email: str,
        gender: int,
        date_of_birth: str,
        hashed_password: str,
        pseudo: str = "",
    ) -> ConnectedUser:

        values = (
            id_user,
            name,
            phone_number,
            email,
            gender,
            date_of_birth,
            hashed_password,
            pseudo,
        )
        user = self.get_user_by_id(id_user)
        if user:
            return user
        try:
            with DBConnection().connection.cursor() as cursor:
                query = f"INSERT INTO users(id_user,name,phone_number,email,gender,date_of_birth, hashed_password,pseudo) VALUES ({', '.join(['%s'] * len(values))})"
                cursor.execute(query, values)
                DBConnection().connection.commit()

        except Exception as e:
            print(f"Erreur lors de l'insertion dans users: {str(e)}")
            DBConnection().connection.rollback()
            return None
        created = ConnectedUser(
            id_user=id_user,
            name=name,
            pseudo=pseudo,
            email=email,
            gender=gender,
            hashed_password=hashed_password,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
        )

        return created

    # READ (Fetch a single user by ID)
    def get_user_by_id(self, id_user) -> ConnectedUser:

        try:
            query = "SELECT * FROM users WHERE id_user = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_user,))
                    res = cursor.fetchone()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
            return None
        if res:
            user_read = ConnectedUser(**res)
            return user_read
        else:
            return None

    # READ (Fetch some users by name)
    def get_user_by_name(self, search_string, size=10) -> List[ConnectedUser]:

        search_string = str(search_string).lower()
        try:
            query = f"SELECT * FROM users WHERE LOWER(name) LIKE %s or LOWER(pseudo) LIKE %s "
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query, ("%" + search_string + "%", "%" + search_string + "%")
                    )
                    results = cursor.fetchmany(size)
        except Exception as e:
            print(f"Error while searching: {e}")
            return None
        if results:
            users_read = [ConnectedUser(**res) for res in results]
        return users_read

    # READ (Fetch all users)
    def get_all_users(self, limit: int = 10, offset: int = 0) -> List[ConnectedUser]:

        try:
            query = f"SELECT * FROM users LIMIT {max(0,limit)} OFFSET {max(offset,0)}"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, ())
                    results = cursor.fetchall()
        except Exception as e:
            print(f"Error while fetching FROM users: {e}")
        if results:
            users_read = [ConnectedUser(**res) for res in results]
        return users_read

    # UPDATE
    def update_user(
        self,
        id_user: int,
        name=None,
        email=None,
        pseudo=None,
        hashed_password=None,
        phone_number=None,
        date_of_birth=None,
        gender=None,
    ):
        try:
            # Build the dynamic query based on the provided parameters
            updates = []
            values = []

            if name:
                updates.append("name = %s")
                values.append(name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if password:
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
            if pseudo:
                updates.append("pseudo = %s")
                values.append(pseudo)

            # If there are no updates, return
            if not updates:
                print("No data provided for update.")
                return None

            query = f"UPDATE users SET {', '.join(updates)} WHERE id_user = %s"
            values.append(id_user)
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    connection.commit()
            print(f"User {id_user} updated successfully!")

        except Exception as e:
            print(f"Error updating user: {e}")

    # DELETE
    def delete_user(self, id_user):
        try:
            query = "DELETE FROM users WHERE id_user = %s"
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        query,
                        (id_user,),
                    )
                    connection.commit()
                    print("Record deleted successfully FROM users.")
        except Exception as e:
            print(f"Error while deleting FROM users: {e}")
            return None
