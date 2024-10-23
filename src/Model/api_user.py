from pydantic import BaseModel


class APIUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    password: str
    email_address: str