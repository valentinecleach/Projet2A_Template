from pydantic import BaseModel


class Genre(BaseModel):
    """
    Class representing a genre with an id and a name.

    Attributes
    ----------
    id : int
        An id that allows easy recognition of the genre
    name : str
        The genre's name

    Examples
    --------
    print(Genre(id=123, name="Musical Comedy"))
    """

    id: int
    name: str

    def __repr__(self):
        """Display method for a genre."""
        return f"Genre(id={self.id}, name='{self.name}')"


# Unrelated code to show sys.path to understand error with classes ipmports.
