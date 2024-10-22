from pydantic import BaseModel
from typing import Dict, Any

class MovieCollection(BaseModel):
    id: int
    name: str
    
    def __str__(self):
        """Méthode d'affichage pour une collection de films."""
        return f"Collection: {self.name} (ID: {self.id})"
        
    def __repr__(self):
        return f"MovieCollection(id={self.id}, name='{self.name}')"