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
        password: str,
        pseudo: str = "",
    ) -> ConnectedUser:

        values = (
            id_user,
            name,
            phone_number,
            email,
            gender,
            date_of_birth,
            password,
            pseudo,
        )

        res = DBConnection().insert(cine.user, values)
        if res:
            created = ConnectedUser(
                name=name,
                pseudo=pseudo,
                email=email,
                gender=gender,
                password=password,  # hacher ce mot de passe
                date_of_birth=date_of_birth,
                phone_number=phone_number,
            )
        return created

    # READ (Fetch a single user by ID)
    def get_user_by_id(self, id_user) -> ConnectedUser:

        res = DBConnection().read_by_id(cine.user, "id_user", id)
        if res:
            user_read = ConnectedUser(
                name=res["name"],
                pseudo=res["pseudo"],
                email=res["email"],
                password=res["password"],
                date_of_birth=res["date_of_birth"],
                phone_number=res["phone_number"],
            )
        return user_read

    # READ (Fetch some users by name)
    def get_user_by_name(self, search_string, size=10) -> List(ConnectedUser):

        results = DBConnection().read_by_string(cine.user, "name", search_string, size)
        if results:
            users_read = [
                ConnectedUser(
                    name=res["name"],
                    pseudo=res["pseudo"],
                    email=res["email"],
                    gender=res["gender"],
                    password=res["password"],
                    date_of_birth=res["date_of_birth"],
                    phone_number=res["phone_number"],
                )
                for res in results
            ]
        return users_read

    # READ (Fetch all users)
    def get_all_users(self, limit: int = 10, offset: int = 0) -> List[ConnectedUser]:

        results = DBConnection().read_all(cine.user, limit, offset)
        if results:
            users_read = [
                ConnectedUser(
                    name=res["name"],
                    pseudo=res["pseudo"],
                    email=res["email"],
                    gender=res["gender"],
                    password=res["password"],
                    date_of_birth=res["date_of_birth"],
                    phone_number=res["phone_number"],
                )
                for res in results
            ]
        return users_read

    # UPDATE
    def update_user(
        self,
        id_user: int,
        name=None,
        email=None,
        pseudo=None,
        password=None,
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
                updates.append("password = %s")
                values.append(password)
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

            query = f"UPDATE cine.user SET {', '.join(updates)} WHERE id_user = %s"
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
        DBConnection().delete(cine.user, "id_user", id_user)
