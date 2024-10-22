from typing import List, Dict, Any
from src.Model.genre import Genre

class GenreService:

    @classmethod
    def from_full_data(cls, data: List[Dict[str, Any]]) -> List[Genre]:
        """Méthode de classe pour créer une liste d'instances de Genre à partir de données complètes.

        Parameters
        ----------
        data : list of dict
            Une liste de dictionnaires, chacun contenant des données de genre.

        Returns
        -------
        List[Genre]
            Une liste d'instances de Genre.
        """
        return [Genre(id=item['id'], name=item['name']) for item in data]

# code to prepare the doctests
genre_service = GenreService()
genre_action = [{"id": 28, "name": "Action"}]
print(genre_service.from_full_data(genre_action))