# src/DAO/MovieMaker_dao.py

from Model.MovieMaker import MovieMaker
from DAO.DBConnection import DBConnection

class MovieMakerDAO:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def insert(self, movie_maker: MovieMaker) -> MovieMaker:
        """
        Insère un nouveau MovieMaker dans la base de données.

        Parameters:
        -----------
        movie_maker : MovieMaker
            L'objet MovieMaker à insérer.

        Returns:
        --------
        MovieMaker
            L'objet MovieMaker inséré, avec son ID.
        """
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO movie_makers (id_movie_maker, adult, name, gender, biography,
                                            birthday, place_of_birth, deathday, known_for_department,
                                            popularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (movie_maker.id_movie_maker, movie_maker.adult, movie_maker.name,
                    movie_maker.gender, movie_maker.biography, movie_maker.birthday,
                    movie_maker.place_of_birth, movie_maker.deathday,
                    movie_maker.known_for_department, movie_maker.popularity))
                # movie_maker.id_movie_maker = cursor.fetchone()['id_movie_maker'] if we don't want the same id as the one they have on TMDB.
                # ajouter Returning dans le query si on veut générer un id
                self.db_connection.connection.commit()
                print("Insersion successful : MovieMaker added.")
        except Exception as e:
            print("Insersion error : ", str(e))

    def update(self, movie_maker: MovieMaker):
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE MovieMaker
                    SET adult = %s, name = %s, gender = %s, biography = %s,
                        birthday = %s, place_of_birth = %s, deathday = %s,
                        known_for_department = %s, popularity = %s
                    WHERE id_movie_maker = %s;
                """, (movie_maker.adult, movie_maker.name, movie_maker.gender,
                      movie_maker.biography, movie_maker.birthday,
                      movie_maker.place_of_birth, movie_maker.deathday,
                      movie_maker.known_for_department, movie_maker.popularity,
                      movie_maker.id_movie_maker))

                self.db_connection.connection.commit()
                print("Update successful : MovieMaker updated.")
        except Exception as e:
            print("Update error : ", str(e))

    def delete(self, id_movie_maker: int):
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM MovieMaker
                    WHERE id_movie_maker = %s;
                """, (id_movie_maker,))

                self.db_connection.connection.commit()
                print("Deletion successful : MovieMaker deleted.")
        except Exception as e:
            print("Delete error : ", str(e))

    def get_by_id(self, id_movie_maker: int) -> MovieMaker | None:
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM MovieMaker
                    WHERE id_movie_maker = %s;
                """, (id_movie_maker,))
                result = cursor.fetchone()
                if result:
                    return MovieMaker(**result)
                else:
                    print("NO MovieMaker with this id.")
                    return None
        except Exception as e:
            print("Error during recovery by id : ", str(e))
            return None

    def get_by_name(self, name: str) -> list[MovieMaker]:
        try:
            with self.db_connection.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM MovieMaker
                    WHERE name ILIKE %s;  -- ILIKE for case-insensitive searching
                """, (f"%{name}%",))
                results = cursor.fetchall()
                return [MovieMaker(**row) for row in results] if results else []
        except Exception as e:
            print("Error during recovery by name : ", str(e))
            return [] # empty list to concerve typing : supposed to be a list of MovieMaker

