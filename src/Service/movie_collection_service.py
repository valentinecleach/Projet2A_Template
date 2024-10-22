from typing import List, Dict, Any
from src.Model.movie_collection import MovieCollection

class MovieCollectionService:

    @classmethod
    def from_full_data(cls, data: Dict[str, Any]) -> 'MovieCollection':
        """Méthode de classe pour créer une instance à partir de données complètes.
        
        Parameters:
        ----------
        data : dict
            Un dictionnaire contenant toutes les données, dont certaines peuvent être ignorées.
        
        Returns:
        -------
        MovieCollection
            Une instance de MovieCollection contenant uniquement l'id et le nom.
        """
        return [MovieCollection(id=data['id'], name=data['name'])]

movie_collection_service = MovieCollectionService()
# print(movie_collection_service.create_list_of_collection({'id': 87096, 'name': 'Avatar Collection', 'poster_path': '/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg', 'backdrop_path': '/gxnvX9kF7RRUQYvB52dMLPgeJkt.jpg'}))
x = movie_collection_service.from_full_data({'id': 87096, 'name': 'Avatar Collection', 'poster_path': '/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg'})
for k in x :
    print(k)