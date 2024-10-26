from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.genre import Genre


class GenreDao(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def insert(self, new_genre: Genre): 
        try:
            """
            Ajoute un genre dans la base de données.

            Paramètres:
            -----------
            new_genre : Genre
                Le genre à ajouter dans le schéma.
            """
            # Vérification de l'existence du genre
            query = "SELECT id_genre FROM genre WHERE id_genre = %s;"
            genre_exists = self.db_connection.sql_query(query, (new_genre.id,), return_type="one")

            if genre_exists is None:
                insert_query = """
                    INSERT INTO Genre (id_genre, name_genre)
                    VALUES (%s, %s);
                """
                self.db_connection.sql_query(insert_query, (new_genre.id, new_genre.name,))
                print("Insertion successful: Genre added.")
            else:
                print(f"Genre with id {new_genre.id} already exists.")

        except Exception as e:
            print("Insertion error: ", str(e))



# works : add a new genre in the schema
# mon_objet = GenreDao()
# mon_objet.insert(Genre(id =  28, name = "Action"))
