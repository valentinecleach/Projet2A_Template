# ORM avec framework comme SQLAlchemy fait lesrequêtes pour nous. Mais pas le but du projet info

import psycopg2
from psycopg2.extras import RealDictCursor

class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self, test : bool):
        dotenv.load_dotenv(override=True)
        self.__connection = psycopg2.connect(
            host=os.environ["host"],
            port=os.environ["port"],
            dbname=os.environ["dbname"],
            user=os.environ["user"],
            password=os.environ["password"],
            cursor_factory=RealDictCursor,
        )
        if not test :
            self.__set_search_path(os.environ["pro"]) 
        else:
            self.__set_search_path(os.environ["test"])  # change with schema projet_info_test for tests. 

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
        Creates the MovieMaker table in the database if it does not exist.
        """
        create_table_MovieMaker = """
        CREATE TABLE IF NOT EXISTS MovieMaker (
            id_movie_maker SERIAL PRIMARY KEY,
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
            id_user SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,  
            email VARCHAR(255) UNIQUE NOT NULL
        );
        """
        # add query for the creation of ither tables 
        with self.db_connection.connection.cursor() as cursor:
            cursor.execute(create_table_MovieMaker)
            cursor.execute(create_table_users)
            # add cursor.execute( other tables)
            self.db_connection.connection.commit()

    def insert(self, table_name: str, values: tuple):
        """Insère des données dans une table spécifiée en récupérant les colonnes dynamiquement."""
        try:
            with self.__connection.cursor() as cursor:
                # Récupérer la liste des colonnes de la table
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (table_name,))
                columns = [row['column_name'] for row in cursor.fetchall()]

                # Crée une chaîne de requête d'insertion avec des placeholders
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
                cursor.execute(query, values)
                self.__connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'insertion dans {table_name}: {str(e)}")
            self.__connection.rollback()