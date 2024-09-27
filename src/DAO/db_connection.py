import psycopg2
from getpass import getpass

class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Open the connection.
        self.__connection = psycopg2.connect(
            host=os.environ["sgbd-eleves.domensai.ecole"],
            port=os.environ["5432"],
            dbname=os.environ["id2464"],
            user=os.environ["id2464"],
            password=os.environ["id2464"],
            cursor_factory=RealDictCursor, # permet de récupérer les résultats des requêtes sous forme de dictionnaire et non de tupple
        )

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection

 