from pydantic import BaseModel


class User(BaseModel):
    """user in the system, with an optional ip_address

    Attributes
    ----------
    ip_adress: str
        representing an IP address if defined
    """

    ip_address: str | None = None

    class Config:
        # Options de configuration supplémentaires si nécessaire
        pass
