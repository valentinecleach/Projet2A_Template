class MovieCollection:
    """
    Class representing the collection of the movie.

    Parameters
    ----------
    id : int
        The id of the collection
    name : str
        The name of the collection

    Examples
    --------
    

    """

    def __init__(self, MovieCollection_data: dict):
        """Constructor

        Parameters:
        -----------
        MovieCollection_data : dict
            A dictionary containing the collection of the movie data (id_user and id_Movie).
        """
        self.id = MovieCollection_data.get("id")
        self.name = MovieCollection_data.get("name")

    def __repr__(self):
       return f" 'Movie Collection : {self.name}' "


# Unrelated code to show sys.path to understand error with classes ipmports.


# code to prepare the doctests
avatar_collection = {
		"id": 87096,
		"name": "Avatar Collection",
		"poster_path": "/uO2yU3QiGHvVp0L5e5IatTVRkYk.jpg",
		"backdrop_path": "/gxnvX9kF7RRUQYvB52dMLPgeJkt.jpg"
	}

print(MovieCollection(avatar_collection))
