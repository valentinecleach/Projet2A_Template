from typing import List  # , Optional

from DAO.db_connection import DBConnection, Singleton
from Model.connected_user import ConnectedUser


class UserDAO(metaclass=Singleton):
    # CREATE
    def create_user(
        self,
        id_user: int,
        name: str,
        phone_number: str,
        email_address: str,
        gender: int,
        birthday: str,
        password: str,
    ):

        values = (
            id_user,
            name,
            phone_number,
            email_address,
            gender,
            birthday,
            password,
        )

        DBConnection().insert(self, user, values)

    # READ (Fetch a single user by ID)
    def get_user_by_id(self, id_user):

        return DBConnection().read_by_id(self, user, "id_user", id)

    # READ (Fetch all users)
    def get_all_users(self):

        return DBConnection().read_by_id(self, user)

    # UPDATE
    def update_user(
        self,
        id_user: int,
        name=None,
        email_address=None,
        password=None,
        phone_number=None,
        birthday=None,
        gender=None,
    ):
        try:
            # Build the dynamic query based on the provided parameters
            updates = []
            values = []

            if name:
                updates.append("name = %s")
                values.append(name)
            if email_address:
                updates.append("email_address = %s")
                values.append(email_address)
            if password:
                updates.append("password = %s")
                values.append(password)
            if phone_number:
                updates.append("phone_number = %s")
                values.append(phone_number)
            if birthday:
                updates.append("birthday = %s")
                values.append(birthday)
            if gender:
                updates.append("gender = %s")
                values.append(gender)

            # If there are no updates, return
            if not updates:
                print("No data provided for update.")
                return

            query = f"UPDATE user SET {', '.join(updates)} WHERE id_user = %s"
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
        DBConnection().delete(user, "id_user", id_user)
