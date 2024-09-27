# ORM avec framework comme SQLAlchemy fait lesrequêtes pour nous. Mais pas le but du projet info

import psycopg2
from psycopg2.extras import RealDictCursor

class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Open the connection.
        self.__connection = psycopg2.connect(
            host=os.environ["host"],
            port=os.environ["port"],
            dbname=os.environ["dbname"],
            user=os.environ["user"],
            password=os.environ["password"],
            cursor_factory=RealDictCursor, # permet de récupérer les résultats des requêtes sous forme de dictionnaire et non de tupple
        )

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection

 