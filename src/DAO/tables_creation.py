from src.DAO.db_connection import DBConnection
from src.DAO.singleton import Singleton

class TablesCreation(metaclass=Singleton):
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection
        self.create_tables()

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
                overview TEXT,
                popularity FLOAT,
                release_date DATE,
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
            create_table_Movie_Collection = """
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
                username VARCHAR(255) unique NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) ,
                token VARCHAR(255) NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                email_address VARCHAR(255) UNIQUE NOT NULL,
                date_of_birth DATE, 
                phone_number VARCHAR(255),
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
                comment TEXT NOT NULL, -- le commentaire ne doit probablement pas être vide
                date DATE NOT NULL, -- ajouter NOT NULL pour la date

                FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE, -- pour gérer la suppression d'utilisateurs
                FOREIGN KEY (id_movie) REFERENCES movie(id_movie) ON DELETE CASCADE -- pour gérer la suppression de films
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
                id_movie INTEGER,
                id_movie INTEGER,

                FOREIGN KEY (id_maker) REFERENCES movie_maker(id_movie_maker),
                FOREIGN KEY (id_movie) REFERENCES movie(id_movie)
            );
            """

            create_table_user_movie_collection = """
            CREATE TABLE IF NOT EXISTS user_movie_collection (
                id_user INTEGER NOT NULL,
                id_movie INTEGER NOT NULL,
                date VARCHAR(255) NOT NULL,

                PRIMARY KEY (id_movie, id_user), 
                FOREIGN KEY (id_movie) REFERENCES movie(id_movie),
                FOREIGN KEY (id_user) REFERENCES users(id_user)
            );
            """

            # add query for the creation of ither tables
            with self.db_connection.connection as connection:
                # Creation of a cursor for the request
                with connection.cursor() as cursor:
                    cursor.execute(create_table_Genre)
                    cursor.execute(create_table_Movie)
                    cursor.execute(create_table_Movie_Collection)
                    cursor.execute(create_table_Link_Movie_MovieCollection)
                    cursor.execute(create_table_Link_Movie_Genre)
                    cursor.execute(create_table_users)
                    cursor.execute(create_table_comment)         
                connection.commit()
