import os
from typing import Literal, Optional, Union
import dotenv

import psycopg2
from psycopg2.extras import RealDictCursor


class DBConnector:
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
        return_type: Union[Literal["one"], Literal["all"]] = "one"
    ):
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
                    if query.strip().upper().startswith(("CREATE","INSERT", "UPDATE", "DELETE")):
                        connection.commit()
                        return None
                    if return_type == "one":
                        return cursor.fetchone()
                    if return_type == "all":
                        return cursor.fetchall()
        except Exception as e:
            print("ERROR")
            print(e)
            raise e


