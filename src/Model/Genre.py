class Genre:
    """
    Class representing a genre with an id and a name.

    Parameters
    ----------
    id : int
        An id that allows easy recognition of the genre
    name : str
        The genres name

    Examples
    --------
    print(Genre(genre_data={'id': 123, 'name': "Musical Comedy"}))

    """
    def __init__(self, genre_data: dict):
        """Constructor

        Parameters:
        -----------
        genre_data : dict
            A dictionary containing the genre data (id and name).
        """
        self.id = genre_data.get('id')
        self.name = genre_data.get('name')

    def __repr__(self):
       return f"'Genre : {self.name}'"

# Unrelated code to show sys.path to understand error with classes ipmports.

# code to prepare the doctests
genre_action = {
			"id": 28,
			"name": "Action"
		}
print(Genre(genre_data=genre_action))

