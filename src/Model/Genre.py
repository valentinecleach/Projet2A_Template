class Genre:
    def __init__(self, genre_data: dict):
        """
        Class representing a genre with an id and a name.

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
"""
import sys

# Affiche tout ce qui est dans sys.path
for path in sys.path:
    print(path)
"""