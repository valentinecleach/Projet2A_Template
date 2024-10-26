from src.DAO.db_connection import DBConnector  

class UserFollowDAO:
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection

    def insert(self, user_id: int, follow_user_id: int):
        """Insert a follow relationship between users if it doesn't already exist."""
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM user_follow 
                WHERE user_id = %s AND follow_user_id = %s;
            """
            result = self.db_connection.sql_query(query, (user_id, follow_user_id,), return_type="one")
            
            # Vérifiez si la relation existe
            follow_exists = result["count"] > 0 if result else False

            if not follow_exists:
                print("Inserting follow relationship.")
                insert_query = """
                    INSERT INTO user_follow (user_id, follow_user_id)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (user_id, follow_user_id,))
                print("Insertion successful: Follow relationship added.")
            else:
                print("Follow relationship already exists, no insertion performed.")

        except Exception as e:
            print("Insertion error: ", str(e))



