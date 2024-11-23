from pydantic import BaseModel


class JWTResponse(BaseModel):
    """A Json Web Token Response

    Parameters
    ----------
    acess_token: str
        Access token encapsulation for authentication 
    """
    access_token: str