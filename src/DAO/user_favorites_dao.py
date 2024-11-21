from datetime import datetime

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.movie_dao import MovieDAO

class UserFavoriteDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        self.db_connection = db_connection

    def insert(self, id_user: int, id_movie: int):
        """Insert a favorite relationship between a user and a movie into user_movie_collection if it doesn't already exist."""
        try:
            # Vérification de l'existence de la relation
            query = """
                SELECT COUNT(*) as count FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """
            result = self.db_connection.sql_query(
                query,
                (id_user, id_movie),
                return_type="one",
            )

            favorite_exists = result["count"] > 0 if result else False

            if not favorite_exists:
                print("Inserting favorite relationship.")
                insert_query = """
                    INSERT INTO user_movie_collection (id_user, id_movie, date)
                    VALUES (%s, %s, %s);
                """
                the_date = datetime.now().date()
                values = (id_user, id_movie, the_date)
                self.db_connection.sql_query(insert_query, values)
                print("Insertion successful: Favorite relationship added.")
            else:
                print("Favorite relationship already exists, no insertion performed.")
        except Exception as e:
            print("Insertion error:", str(e))

    def remove(self, id_user: int, id_movie: int):
        """Supprime un film des favoris d'un utilisateur."""
        try:
            delete_query = """
                DELETE FROM user_movie_collection
                WHERE id_user = %s AND id_movie = %s;
            """
            self.db_connection.sql_query(delete_query, (id_user, id_movie))
            print("Deletion successful: Movie removed from favorites.")
        except Exception as e:
            print("Deletion error:", str(e))

    def get_favorites(self, id_user: int):
        """Récupère la liste des films favoris d'un utilisateur."""
        try:
            select_query = """
                SELECT id_movie, date FROM user_movie_collection
                WHERE id_user = %s
                ORDER BY date DESC;
            """
            results = self.db_connection.sql_query(
                select_query, (id_user,), return_type="all"
            )
            if results:
                mov = MovieDAO(self.db_connection)
                return [mov.get_by_id(res["id_movie"]) for res in results]
        except Exception as e:
            print("Retrieval error:", str(e))
            return []
