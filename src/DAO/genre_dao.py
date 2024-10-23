from typing import Dict, List, Optional

from psycopg2.extras import DictCursor

from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton
from src.Model.genre import Genre


class GenreDao(metaclass=Singleton):
    def __init__(self):
        # Créer un objet de connexion à la base de données
        self.db_connection = DBConnection()
        # Créer des tables si elles n'existent pas
        self.db_connection.create_tables()

<<<<<<< HEAD
    def insert(self, new_genre):
=======

    def insert(self, new_genre: Genre): 
>>>>>>> f2272497c1151fa36673e92207a5cfe5f29a9a58
        try:
            """
            Ajoute un genre dans la base de données.

            Paramètres:
            -----------
            new_genre : Genre
                Le genre à ajouter dans le schéma.
            """
            # Connexion
            with self.db_connection.connection as connection:
                # Création d'un curseur pour la requête
                with connection.cursor() as cursor:
<<<<<<< HEAD
                    # SQL resquest
                    cursor.execute(
                        "SELECT id_genre FROM genre WHERE id_genre = %s",
                        (new_genre.id,),
=======
                    # Requête SQL pour vérifier l'existence du genre
                    cursor.executed(
                        'SELECT id_genre FROM genre WHERE id_genre = %s',
                         (28,)
>>>>>>> f2272497c1151fa36673e92207a5cfe5f29a9a58
                    )
                    genre_exists = cursor.fetchone()

                    if genre_exists is None:
                        cursor.execute(
                            """
                            INSERT INTO Genre (id_genre, name_genre)
                            VALUES (%s, %s)
                            """,
<<<<<<< HEAD
                            (new_genre.id, new_genre.name),
=======
                            (new_genre.id, new_genre.name)
>>>>>>> f2272497c1151fa36673e92207a5cfe5f29a9a58
                        )
                        connection.commit()
                        print("Insertion successful : Genre added.")
                    else:
                        print(f"Genre with id {new_genre.id} already exists.")
        except Exception as e:
            print("Insertion error : ", str(e))
<<<<<<< HEAD


# works : add a new genre in the schema
# mon_objet = GenreDao()
# mon_objet.insert(Genre(id =  28, name = "Action"))
=======
>>>>>>> f2272497c1151fa36673e92207a5cfe5f29a9a58
