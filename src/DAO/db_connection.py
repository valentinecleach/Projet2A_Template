# ORM avec framework comme SQLAlchemy fait lesrequêtes pour nous.
import os

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from src.DAO.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self, test: bool):
        dotenv.load_dotenv(override=True)
        self.__connection = psycopg2.connect(
            host=os.environ["host"],
            port=os.environ["port"],
            dbname=os.environ["dbname"],
            user=os.environ["user"],
            password=os.environ["password"],
            cursor_factory=RealDictCursor,
        )
        if not test:
            self.__set_search_path(os.environ["pro"])
        else:
            self.__set_search_path(
                os.environ["test"]
            )  # change with schema projet_info_test for tests.

    def __set_search_path(self, schema: str):
        """
        Sets the search path to the provided schema.
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(f"SET search_path TO {schema};")
        self.__connection.commit()

    @property
    def connection(self):
        return self.__connection

    def create_tables(self):
        """
        Creates the movie_maker table in the database if it does not exist.
        """
        create_table_movie_maker = """
        CREATE TABLE IF NOT EXISTS movie_maker (
            id_movie_maker INTEGER PRIMARY KEY,
            adult BOOLEAN NOT NULL DEFAULT FALSE,
            name VARCHAR(255) NOT NULL,
            gender INTEGER NOT NULL,
            biography TEXT NOT NULL,
            birthday DATE,
            place_of_birth VARCHAR(255),
            deathday DATE,
            known_for_department VARCHAR(255),
            popularity FLOAT NOT NULL,
            known_for JSONB
        );
        """

        create_table_user = """
        CREATE TABLE IF NOT EXISTS user (
            id_user INTEGER PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,  
            email VARCHAR(255) UNIQUE NOT NULL
        );
        """

        create_table_movie = """
        CREATE TABLE IF NOT EXISTS movie (
            id_movie INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            budget FLOAT,
            adult BOOLEAN NOT NULL DEFAULT FALSE,
            origine_country LIST,
            original_language VARCHAR(255),
            original_title VARCHAR(255),
            overwiev VARCHAR(255),
            popularity FLOAT,
            release_date VARCHAR(255),
            revenue INTEGER,
            vote_average FLOAT,
            vote_count INTEGER,
            status VARCHAR(255)
        );
        """

        create_table_movie_genre = """
        CREATE TABLE IF NOT EXISTS movie_Genre (
            id_movie INTEGER NOT NULL FOREIGN KEY,
            id_genre INTEGER NOT NULL FOREIGN KEY

            FOREIGN KEY (id_genre) REFERENCES Genre(id_genre)
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        create_table_Genre = """
        CREATE TABLE IF NOT EXISTS GENRE (
            id_genre INTEGER NOT NULL PRIMARY KEY,
            genre_name VARCHAR(255),
        );
        """

        create_table_rating = """
        CREATE TABLE IF NOT EXISTS rating (
            id_user INTEGER NOT NULL,
            id_movie INTEGER NOT NULL,
            rating INTEGER,
            date VARCHAR(255),

            FOREIGN KEY (id_user) REFERENCES user(id_user),
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        create_table_comment = """
        CREATE TABLE IF NOT EXISTS comment (
            id_user INTEGER NOT NULL,
            id_movie INTEGER NOT NULL,
            comment TEXT,
            date VARCHAR(255),

            FOREIGN KEY (id_user) REFERENCES user(id_user),
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        create_table_Follower = """
        CREATE TABLE IF NOT EXISTS Follower (
            id_user INTEGER,
            id_user_followed INTEGER,
            date VARCHAR(255),

            FOREIGN KEY (id_user) REFERENCES user(id_user)
        );
        """

        create_table_user_collection = """
        CREATE TABLE IF NOT EXISTS user_collection(
            id_user INTEGER NOT NULL,
            id_collection INTEGER NOT NULL,
            date VARCHAR(255),

            FOREIGN KEY (id_user) REFERENCES user_collection(id_user),
            FOREIGN KEY (id_collection) REFERENCES movie(id_collection)
        );
        """

        create_table_movie_collection = """
        CREATE TABLE IF NOT EXISTS movie_collection (
            id_user INTEGER,
            id_movie INTEGER,

            FOREIGN KEY (id_user) REFERENCES user(id_user),
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        create_table_KnownFor = """
        CREATE TABLE IF NOT EXISTS KnownFor (
            id_movie_maker INTEGER,
            id_movie INTEGER,

            FOREIGN KEY (id_maker) REFERENCES movie_maker(id_movie_maker),
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        # add query for the creation of ither tables
        with self.db_connection.connection.cursor() as cursor:
            cursor.execute(create_table_movie_maker)
            cursor.execute(create_table_user)
            # add cursor.execute( other tables)
            self.db_connection.connection.commit()

    # create
    def insert(self, table_name: str, values: tuple):
        """Insère des données dans une table spécifiée en récupérant les colonnes dynamiquement."""
        try:
            with self.__connection.cursor() as cursor:
                # Récupérer la liste des colonnes de la table
                cursor.execute(
                    f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name = %s
                """,
                    (table_name,),
                )
                columns = [row["column_name"] for row in cursor.fetchall()]

                # Crée une chaîne de requête d'insertion avec des placeholders
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
                cursor.execute(query, values)
                self.__connection.commit()
                return 1
        except Exception as e:
            print(f"Erreur lors de l'insertion dans {table_name}: {str(e)}")
            self.__connection.rollback()
            return None

    # READ (Fetch a single row by ID)
    def read_by_id(self, table, id_column, id_value):
        try:
            query = f"SELECT * FROM {table} WHERE {id_column} = %s"
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_value,))
                    result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error while fetching from {table}: {e}")
            return None

    def read_all_by_id(self, table, id_column, id_value):
        try:
            query = f"SELECT * FROM {table} WHERE {id_column} = %s"
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_value,))
                    result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error while fetching from {table}: {e}")
            return None

    # READ (Fetch rows by name)
    def read_by_string(self, table, search_column, search_string, size=10):
        """
        Searches for records in a table based on a string.

        :param table: Name of the table in which to perform the search.
        :param search_column: The column to search.
        :param search_string: The string to search for.
        :return: The corresponding results.
        """
        search_string = str(search_string).lower()
        try:
            query = f"SELECT * FROM {table} WHERE LOWER({search_column}) LIKE %s"
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, ("%" + search_string + "%",))
                    results = cursor.fetchmany(size)
            return results
        except Exception as e:
            print(f"Error while searching: {e}")
            return None

    # Read many
    def read_all(self, table, limit: int = 10, offset: int = 0):
        try:
            query = (
                f"SELECT * FROM {table} LIMIT {max(limit, 0)} OFFSET {max(offset, 0)}"
            )
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error while fetching all records from {table}: {e}")
            return None

    # UPDATE
    def update(self, table, id_column, id_value, update_columns, update_values):
        try:
            set_clause = ", ".join([f"{col} = %s" for col in update_columns])
            query = f"UPDATE {table} SET {set_clause} WHERE {id_column} = %s"
            values = update_values + [id_value]
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, tuple(values))
                    connection.commit()
                    print(f"Record updated successfully in {table}.")
        except Exception as e:
            print(f"Error while updating {table}: {e}")
            return None

    # DELETE
    def delete(self, table, id_column, id_value):
        try:
            query = f"DELETE FROM {table} WHERE {id_column} = %s"
            with self.connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (id_value,))
                    connection.commit()
                    print(f"Record deleted successfully from {table}.")
        except Exception as e:
            print(f"Error while deleting from {table}: {e}")
            return None
