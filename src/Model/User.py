from pydantic import BaseModel


class User(BaseModel):
    """A user in the system, with an optional ip_address

    Attributes
    ----------
    ip_adress : str, optional
        Represents an IP address if defined
    """

    ip_address: str | None = None

    class Config:
        # Additional configuration options if needed
        pass
