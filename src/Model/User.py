from pydantic import BaseModel


class User(BaseModel):
    ip_address: str | None = None

    class Config:
        # Options de configuration supplémentaires si nécessaire
        pass
