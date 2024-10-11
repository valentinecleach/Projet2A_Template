from typing import List, Optional

from DAO.db_connection import DBConnection
from Model.Movie import Movie


# A Faire: (valentine)
class Movie_dao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def insert(self, new_movie: Movie):
        """
        Adds a movie into the database.

        Parameters:
        -----------
        new_movie : Movie
            A new movie to add to the database

        """
        # if new_movie.id already exists do an error.
        # Connexion
        with DBconnection().connection as connection:
            # Creation of a cursor for the request
            with connextion.cursor() as cursor:
                # SQL resquest
                cursor.execute("""
                    INSERT INTO Movie (adult, genre_ids, id, original_title, overview, 
                                        popularity, release_date, title, vote_average, 
                                        vote_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                               (new.movie.adult, new.movie.genre.id, new.movie.original_title, new.movie.overview,
                               new.movie.popularity, new.movie.release_date, new.movie.title, new.movie.vote_average,
                               new.movie.vote))
                               # tagline? status?)
            # Fetching the result
            res = cursor.fetchone()
            
        # if we have a result
        if res:
            pass
            # what_we_returne = 
            print("Insertion successful : Movie added.")
        except Exception as e:
            print("Insertion error : ", str(e))
        return None #what_we_return

    def update(self, movie : Movie):
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Movie
                    SET adult = %s, genre.id = %s , original_title = %s, overview = %s,
                               popularity = %s, release_date = %s, title = %s, vote_average = %s,
                               vote = %s
                    WHERE id_movie = %s;
                """, (movie.adult, movie.genre.id, movie.original_title, movie.overview,
                               movie.popularity, movie.release_date, movie.title, movie.vote_average,
                               movie.vote))
                self.db_connection.connection.commit()
                print("Update successful : movie updated.")
        except Exception as e:
            print("Update error : ", str(e))


    def delete(self, id_movie: int):
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM Movie
                    WHERE id_movie = %s;
                """, (id_movie,))

                self.db_connection.connection.commit()
                print("Deletion successful : Movie deleted.")
        except Exception as e:
            print("Delete error : ", str(e))

    # structure prise du TP
    def find_Movie_by_id(self, id: int) -> Movie:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "SELECT *                                  "
                        "  FROM Movie                 "
                        f"  WHERE id_movie = {id}"
                    )
                    res = cursor.fetchone()
                except Exception as e:
                    print(f" Erreur : {e}")
                    return None
                return res


    def get_by_name(self, name: str) -> list[Movie]:
            try:
                with self.db_connection.connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT * FROM Movie
                        WHERE name ILIKE %s;  -- ILIKE for case-insensitive searching
                    """, (f"%{name}%",))
                    results = cursor.fetchall()
                    return [Movie(**row) for row in results] if results else []
            except Exception as e:
                print("Error during recovery by name : ", str(e))
                return []  # empty list to concerve typing : supposed to be a list of Movie
                
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

# https://api.themoviedb.org/3/search/movie?query=bullet%20train&include_adult=false&language=en-US&page=1
"""
{
  "page": 1,
  "results": [
    {
      "adult": false,
      "backdrop_path": "/y2Ca1neKke2mGPMaHzlCNDVZqsK.jpg",
      "genre_ids": [
        28,
        35,
        53
      ],
      "id": 718930,
      "original_language": "en",
      "original_title": "Bullet Train",
      "overview": "Unlucky assassin Ladybug is determined to do his job peacefully after one too many gigs gone off the rails. Fate, however, may have other plans, as Ladybug's latest mission puts him on a collision course with lethal adversaries from around the globe—all with connected, yet conflicting, objectives—on the world's fastest train.",
      "popularity": 63.204,
      "poster_path": "/tVxDe01Zy3kZqaZRNiXFGDICdZk.jpg",
      "release_date": "2022-08-03",
      "title": "Bullet Train",
      "video": false,
      "vote_average": 7.456,
      "vote_count": 6075
    }
"""