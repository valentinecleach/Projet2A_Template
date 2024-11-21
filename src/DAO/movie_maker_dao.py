# src/DAO/movie_maker_dao.py
from typing import List, Optional

from src.DAO.db_connection import DBConnector
from src.DAO.singleton import Singleton
from src.DAO.known_for_dao import KnownForDao
from src.Model.movie_maker import MovieMaker
from src.DAO.movie_dao import MovieDAO


# to do : Documentation
class MovieMakerDAO(metaclass=Singleton):
    def __init__(self, db_connection: DBConnector):
        # create a DB connection object
        self.db_connection = db_connection
        self.known_for_dao = KnownForDao(db_connection)
        self.movie_dao = MovieDAO(db_connection)

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
                SELECT COUNT(*)
                FROM movie_maker
                WHERE name = %s;
            """
            result = self.db_connection.sql_query(query, (movie_maker.name,), return_type = "one")
            movie_maker_exist = result["count"] > 0
            if not movie_maker_exist:
                print(f"Inserting Movie Maker {movie_maker.name} in the database.")
                query = """
                INSERT INTO movie_maker (id_movie_maker, adult, name, gender, biography,
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
                        )
                self.db_connection.sql_query(query, values)
                print("Insersion successful : MovieMaker added.")
                if movie_maker.known_for:
                    for movie in movie_maker.known_for:
                        self.known_for_dao.insert(movie.id_movie, movie_maker.id_movie_maker)
                    print(f"Known for linked added for {movie_maker.name}")
        except Exception as e:
            print("Insersion error : ", str(e))

    def update(self, movie_maker: MovieMaker):
        try:
            query = """UPDATE movie_maker
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
                DELETE FROM movie_maker
                WHERE id_movie_maker = %s;
                """
            value= (id_movie_maker,)
            self.db_connection.sql_query(query, value)
            print("Deletion successful : MovieMaker deleted.")
        except Exception as e:
            print("Delete error : ", str(e))


    def get_by_name(self, name: str) -> Optional[List[MovieMaker]]:
        try:
            query = """
                    SELECT * FROM movie_maker
                    WHERE name ILIKE %s;
                """
            value = (f"%{name}%",)
            results = self.db_connection.sql_query(query, value, return_type="all")
            if not results:
                print(f"No movie maker found with name: {name} in the database")
                return None
            else:
                movie_makers = []
                for result in results:
                    movie_maker = dict(result)
                    movie_query = """
                        SELECT id_movie
                        FROM knownfor kf
                        WHERE kf.id_movie_maker = %s;
                    """
                    movie_results = self.db_connection.sql_query(movie_query, (movie_maker['id_movie_maker'],), return_type="all")
                    movie_ids = [movie['id_movie'] for movie in movie_results]
                    known_for = []
                    for movie_id in movie_ids:
                        known_for.append(self.movie_dao.get_by_id(movie_id))
                    movie_maker.update({'known_for': known_for})
                    movie_makers.append(MovieMaker(**movie_maker))
            return movie_makers
        except Exception as e:
            print("Error during retrieval by name in the database:", str(e))
            return None

    # def get_by_id(self, id_movie_maker: int) -> MovieMaker | None:   # faire à la fin si temps sinon on l'enlève.
    #     try:
    #         query = """
    #                 SELECT * FROM movie_maker
    #                 WHERE id_movie_maker = %s;
    #             """
    #         value = (id_movie_maker,)
    #         result = self.db_connection.sql_query(query, value, return_type="one")
    #         if result:
    #             the_movie_maker = dict(result)
    #             return MovieMaker(**the_movie_maker)
    #         else:
    #             print(f"NO MovieMaker with the id {id_movie_maker} in the database.")
    #             return None
    #     except Exception as e:
    #         print("Error during recovery by id : ", str(e))
    #         return None

# db_connection = DBConnector()
# my_object = MovieMakerDAO(db_connection)
# print(my_object.get_by_name("james cameron"))
