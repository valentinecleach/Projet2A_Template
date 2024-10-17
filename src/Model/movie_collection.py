class MovieCollection:
    """
    Class representing the collection of the movie.

    Parameters
    ----------
    id_user : int
        An id that allows easy recognition of the User
    id_Movie : int
        An id that allows easy recognition of the Movie

    Examples
    --------
    print(MovieCollection(MovieCollection_data={'id_user': 123, 'id_Movie': "001"}))

    """

    def __init__(self, MovieCollection_data: dict):
        """Constructor

        Parameters:
        -----------
        MovieCollection_data : dict
            A dictionary containing the collection of the movie data (id_user and id_Movie).
        """
        self.id_user = MovieCollection_data.get("id_user")
        self.id_Movie = MovieCollection_data.get("id_Movie")

    def __repr__(self):
        return f"MovieCollection(id_user={self.id_user}, id_Movie='{self.id_Movie}')"


# Unrelated code to show sys.path to understand error with classes ipmports.

# code to prepare the doctests
print(MovieCollection(MovieCollection={"id_user": 123, "is_Movie": "Avegers"}))
