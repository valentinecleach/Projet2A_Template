import os
from typing import Literal, Optional, Union

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


class DBConnector:
    """A connector the the database

    Attributes
    ----------
    host : str
        The database host adress.
    port : str or int
        The port number that the database listens.
    database : str
        The name of the database.
    user : str
        The username for authentification.
    password : str
        The password for authentification.
    schema : str
        The schema used in the database.
    """

    def __init__(self, config=None):
        if config is not None:
            self.host = config["host"]
            self.port = config["port"]
            self.database = config["database"]
            self.user = config["user"]
            self.password = config["password"]
            self.schema = config["schema"]
        else:
            dotenv.load_dotenv(override=True)
            self.host = os.environ["host"]
            self.port = os.environ["port"]
            self.database = os.environ["dbname"]
            self.user = os.environ["user"]
            self.password = os.environ["password"]
            self.schema = os.environ["schema"]

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = None,
    ):
        """
        Executes a query in SQL in the database

        Parameters
        ----------
        query : str
            An SQL query to execute
        data : tuple| list | dict] | None
            Data tp use as values in the SQL query
        return_type : Union[Literal["one"], Literal["all"]] | None
            Decides how many rows to return

        Returns
        -------
        dict or list[dict] or None
            If return_type is "one", it returns a dictionary
            If return_type is "all", it returns a list of dictionaries
            If return_type is None or the query doesn't return anything, it returns None
        """
        try:
            with psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                options=f"-c search_path={self.schema}",
                cursor_factory=RealDictCursor,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, data)
                    if (
                        query.strip()
                        .upper()
                        .startswith(("CREATE", "INSERT", "UPDATE", "DELETE"))
                    ):
                        connection.commit()
                    if return_type == "one":
                        return cursor.fetchone()
                    if return_type == "all":
                        return cursor.fetchall()
        except Exception as e:
            print("ERROR")
            print(e)
            raise e
