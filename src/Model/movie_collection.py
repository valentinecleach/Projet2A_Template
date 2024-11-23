from typing import Any, Dict

from pydantic import BaseModel


class MovieCollection(BaseModel):
    """ A collection of movies from the same saga 

    Attributes
    ----------
    id: int
        The ID of the collection
    name: str
        The name of the collection
    """
    id: int
    name: str
    
    def __str__(self):
        """Display method for a film collection."""
        return f"Collection: {self.name} (ID: {self.id})"
        
    def __repr__(self):
        """Display method for a film collection."""
        return f"MovieCollection(id={self.id}, name='{self.name}')"