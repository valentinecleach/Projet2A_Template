# src/DAO/movie_maker_dao.py
from typing import List

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.Model.movie_maker import MovieMaker


# to do : Documentation
class MovieMakerDAO(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection

    def insert(self, movie_maker: MovieMaker) -> MovieMaker:
        """
        Insert a new MovieMaker in the Database.

        Parameters:
        -----------
        movie_maker : MovieMaker
            MovieMaker objet to insert.
        """
        try:
            query = """
            INSERT INTO movie_makers (id_movie_maker, adult, name, gender, biography,
                                            birthday, place_of_birth, deathday, known_for_department,
                                            popularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                        movie_maker.id_movie_maker,
                        movie_maker.adult,
                        movie_maker.name,
                        movie_maker.gender,
                        movie_maker.biography,
                        movie_maker.birthday,
                        movie_maker.place_of_birth,
                        movie_maker.deathday,
                        movie_maker.known_for_department,
                        movie_maker.popularity,
                    ),
            self.db_connection.sql_query(query, values)
            print("Insersion successful : MovieMaker added.")
        except Exception as e:
            print("Insersion error : ", str(e))

    def update(self, movie_maker: MovieMaker):
        try:
            query = """UPDATE MovieMaker
                    SET adult = %s, name = %s, gender = %s, biography = %s,
                        birthday = %s, place_of_birth = %s, deathday = %s,
                        known_for_department = %s, popularity = %s
                    WHERE id_movie_maker = %s;
            """
            values=(
                        movie_maker.adult,
                        movie_maker.name,
                        movie_maker.gender,
                        movie_maker.biography,
                        movie_maker.birthday,
                        movie_maker.place_of_birth,
                        movie_maker.deathday,
                        movie_maker.known_for_department,
                        movie_maker.popularity,
                        movie_maker.id_movie_maker,
                    ),
            self.db_connection.sql_query(query,values)
            print("Update successful : MovieMaker updated.")
        except Exception as e:
            print("Update error : ", str(e))

    def delete(self, id_movie_maker: int):
        try:
            query = """
                DELETE FROM MovieMaker
                WHERE id_movie_maker = %s;
                """
            value= (id_movie_maker,)
            self.db_connection.sql_query(query, value)
            print("Deletion successful : MovieMaker deleted.")
        except Exception as e:
            print("Delete error : ", str(e))

    def get_by_id(self, id_movie_maker: int) -> MovieMaker | None:
        try:
            query = """
                    SELECT * FROM MovieMaker
                    WHERE id_movie_maker = %s;
                """
            value = (id_movie_maker,)
            result = self.db_connection.sql_query(query, value, return_type="one")
            if result:
                the_movie_maker = dict(result)
                return MovieMaker(**the_movie_maker)
            else:
                print(f"NO MovieMaker with the id {id_movie_maker} in the database.")
                return None
        except Exception as e:
            print("Error during recovery by id : ", str(e))
            return None

    def get_by_name(self, name: str) -> List[MovieMaker] | None:
        try:
            query =  """
                    SELECT * FROM MovieMaker
                    WHERE name ILIKE %s;  
                    -- ILIKE for case-insensitive searching
                """
            value = (f"%{name}%",)
            results = self.db_connection.sql_query(query, value, return_type="all")
            if results:
                return [MovieMaker(**dict(movie_maker)) for movie_maker in results] 
            else :
                print(f"No movie maker found with this name : {name}")
                return []
        except Exception as e:
            print("Error during recovery by name : ", str(e))
            return None
