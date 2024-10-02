from typing import List, Optional

from DAO.db_connection import DBConnection
from Model.Movie import Movie


# A Faire: (valentine)
class Movie_dao :
    # structure prise du TP
    def find_Movie_by_id(self, id:int) -> Movie :
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT *                                  "
                        "  FROM tp.attack a                     "
                        f"  WHERE a.id_attack = {id}"
                    )
                    res = cursor.fetchone()
                except Exception as e:
                    print(f" Erreur : {e}")
                    return None
                return res


"""
tout ceci est inclu si on utilisedes with
conn.commit()
cursor.close()
conn.close()

Pour récupérer des élement
cursor.fetchone()
cursor.fetchall()
cursor.fetchmany(size)

Pour modifier
cursor.execute()
"""
