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

 