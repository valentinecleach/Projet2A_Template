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
        return f"Genre(id={self.id}, name='{self.name}')"

# Unrelated code to show sys.path to understand error with classes ipmports.

# code to prepare the doctests
print(Genre(genre_data={'id': 123, 'name': "Musical Comedy"}))



"""
import sys

# Affiche tout ce qui est dans sys.path
for path in sys.path:
    print(path)
"""
