from src.DAO.db_connection import DBConnector  

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
            result = self.db_connection.sql_query(query, (id_user, id_user_followed,), return_type="one")
            
            # Vérifiez si la relation existe
            follow_exists = result["count"] > 0 if result else False

            if not follow_exists:
                print("Inserting follow relationship.")
                insert_query = """
                    INSERT INTO follower (id_user, id_user_followed)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (id_user, id_user_followed,))
                print("Insertion successful: Follow relationship added.")
            else:
                print("Follow relationship already exists, no insertion performed.")

        except Exception as e:
            print("Insertion error: ", str(e))



