from typing import Any, Dict, List

from src.Model.movie_collection import MovieCollection


class MovieCollectionService:

    @classmethod
    def create_list_of_collection(cls, data: Dict[str, Any]) -> 'MovieCollection':
        """Class method to create an instance from complete data.
        
        Parameters:
        ----------
        data : dict
            A dictionary containing all data, some of which may be ignored.
        
        Returns
        -------
        MovieCollection
            An instance of MovieCollection containing id and name only
        """
        if data:
            return [MovieCollection(id=data['id'], name=data['name'])]
        else:
            return None

#movie_collection_service = MovieCollectionService()

#x = movie_collection_service.create_list_of_collection({'id': 87096, 'name': 'Avatar Collection', 'poster_path': '/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg'})
#for k in x :
#    print(k)