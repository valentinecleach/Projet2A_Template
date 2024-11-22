from pydantic import BaseModel


class APIUser(BaseModel):
    """APIUser is a DAO for manage the commentary in the database

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    id_user : int
        The id of the user
   username: str
        the name of the user
    own_film_collection: list
        the film collection of the user 
    follow_list: list
        the user's list of subscriptions
    """
    id_user : int
    username : str
    own_film_collection : list | None = None
    follow_list : list
