from pydantic import BaseModel


class APIUser(BaseModel):
    """APIUser is an object for managing the commentary in the database

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    id_user : int
        The ID of the user
   username : str
        The name of the user
    own_film_collection : list | None
        The film collection of the user 
    follow_list : list
        The user's list of subscriptions
    """
    id_user : int
    username : str
    own_film_collection : list | None = None
    follow_list : list
