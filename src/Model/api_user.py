from pydantic import BaseModel


class APIUser(BaseModel):
    id : int
    username : str
    own_fillm_collection : list | None = None
    follow_list : list
