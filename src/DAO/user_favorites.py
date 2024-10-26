from src.DAO.db_connection import DBConnector

class UserFavorites:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def insert(self, user_id: int, movie_id: int):
        """Insert a favorite movie for a user if it doesn't already exist."""
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM user_favorites 
                WHERE user_id = %s AND movie_id = %s;
            """
            result = self.db_connection.sql_query(query, (user_id, movie_id,), return_type="one")
            
            # Vérifiez si la relation existe
            favorite_exists = result["count"] > 0 if result else False

            if not favorite_exists:
                print("Inserting favorite movie.")
                insert_query = """
                    INSERT INTO user_favorites (user_id, movie_id)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (user_id, movie_id,))
                print("Insertion successful: Movie added to favorites.")
            else:
                print("Favorite movie already exists, no insertion performed.")

        except Exception as e:
            print("Insertion error: ", str(e))
