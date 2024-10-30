from src.DAO.db_connection import DBConnector

class UserFavoritesDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def insert(self, id_user: int, id_movie: int):
        """Insert a favorite movie for a user if it doesn't already exist."""
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM user_movie_collection 
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(query, (id_user,id_movie,), return_type="one")
            
            # Vérifiez si la relation existe
            favorite_exists = result["count"] > 0 if result else False

            if not favorite_exists:
                print("Inserting favorite movie.")
                insert_query = """
                    INSERT INTO user_movie_collection (id_user,id_movie)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (id_user, id_movie,))
                print("Insertion successful: Movie added to favorites.")
            else:
                print("Favorite movie already exists, no insertion performed.")

        except Exception as e:
            print("Insertion error: ", str(e))
