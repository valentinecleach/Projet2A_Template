from typing import Any, Dict

from pydantic import BaseModel


class MovieCollection(BaseModel):
    """ films from the same saga 

    Attributes
    ----------
    id: int
        id of thecollection
    name: str
        name of the collection
    """
    id: int
    name: str
    
    def __str__(self):
        """Display method for a film collection."""
        return f"Collection: {self.name} (ID: {self.id})"
        
    def __repr__(self):
        """Display method for a film collection."""
        return f"MovieCollection(id={self.id}, name='{self.name}')"