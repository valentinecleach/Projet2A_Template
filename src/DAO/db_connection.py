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

    def __init__(self):
        dotenv.load_dotenv(override=True)
        self.__connection = psycopg2.connect(
            host=os.environ["host"],
            port=os.environ["port"],
            dbname=os.environ["dbname"],
            user=os.environ["user"],
            password=os.environ["password"],
            cursor_factory=RealDictCursor,
        )
        self.__set_search_path(os.environ["schema"]) # change .env to work on test schema

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

        create_table_Movie = """
        CREATE TABLE IF NOT EXISTS movie (
            id_movie INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            budget FLOAT,
            origin_country VARCHAR(255)[],
            original_language VARCHAR(255),
            original_title VARCHAR(255),
            overview VARCHAR(255),
            popularity FLOAT,
            release_date VARCHAR(255),
            revenue BIGINT,
            runtime INTEGER,
            vote_average FLOAT,
            vote_count INTEGER,
            adult BOOLEAN NOT NULL DEFAULT FALSE
        );
        """

        create_table_Genre = """
        CREATE TABLE IF NOT EXISTS genre (
            id_genre INTEGER PRIMARY KEY,
            name_genre VARCHAR(255) NOT NULL
        );
        """
        create_table_Movie_Collection ="""
        CREATE TABLE IF NOT EXISTS movie_collection (
            id_movie_collection INTEGER PRIMARY KEY,
            name_movie_collection VARCHAR(255) NOT NULL
        );
        """

        create_table_Link_Movie_MovieCollection = """
        CREATE TABLE IF NOT EXISTS link_movie_movie_collection (
            id_movie INTEGER,
            id_movie_collection INTEGER,

            PRIMARY KEY (id_movie, id_movie_collection), 
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie),
            FOREIGN KEY (id_movie_collection) REFERENCES movie_collection(id_movie_collection)
        );
        """

        create_table_Link_Movie_Genre = """
        CREATE TABLE IF NOT EXISTS link_movie_genre (
            id_movie INTEGER,
            id_genre INTEGER,

            PRIMARY KEY (id_movie, id_genre), 
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie),
            FOREIGN KEY (id_genre) REFERENCES genre(id_genre)
        );
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

        create_table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            pseudo VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            date_of_birth DATE, 
            phone_number VARCHAR(255) UNIQUE NOT NULL,
            gender INTEGER
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

        create_table_KnownFor = """
        CREATE TABLE IF NOT EXISTS KnownFor (
            id_movie_maker INTEGER,
            id_movie INTEGER,

            FOREIGN KEY (id_maker) REFERENCES movie_maker(id_movie_maker),
            FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
        );
        """

        # add query for the creation of ither tables
        with self.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    cursor.execute(create_table_Genre)
                    cursor.execute(create_table_Movie)
                    cursor.execute(create_table_Movie_Collection)          
                    cursor.execute(create_table_Link_Movie_MovieCollection)
                    cursor.execute(create_table_Link_Movie_Genre)
                    cursor.execute(create_table_users)
                connection.commit()

