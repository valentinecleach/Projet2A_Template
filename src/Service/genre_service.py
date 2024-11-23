from typing import Any, Dict, List

from src.Model.genre import Genre


class GenreService:
    """ A Genre object in our service layer."""

    @classmethod
    def create_list_of_genre(cls, data: List[Dict[str, Any]]) -> List[Genre]:
        """Class method for creating a list of Genre instances from complete data.

        Parameters
        ----------
        data : list of dict
            A list of dictionaries, each containing genre data.

        Returns
        -------
        data : List[Genre]
            A list of Genre instances.

        """
        if data:
            return [Genre(id=item["id"], name=item["name"]) for item in data]
        else:
            return []


# code to prepare the doctests
# genre_service = GenreService()
# genre_action = [{"id": 28, "name": "Action"}]
# print(genre_service.create_list_of_genre(genre_action))
