from pydantic import BaseModel


class JWTResponse(BaseModel):
    """
    Parameters
    ----------
    acess_token: str
        access token encapsulation for authentication 
    """
    access_token: str