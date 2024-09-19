from pydantic import BaseModel
from rating import Rating


class Film(BaseModel):
    """Film

    A series of moving pictures, usually shown in a cinema or on television and
    often telling a story

    Parameters:
    -----------
    id : int
        The id of a movie
    title : str
        The original title of a movie
    release_date : str
        The release date of a movie. Its format is YYYY/MM/DD (?)
    country : str
        The movies country (list of contries ? one str of multiple countries)
    genre : str
        The genre
    plot : str
        A description
    budget : float
        The budget in $ (?)
    rating : Rating
        The films rating out of ...

    Examples
    --------

    """

    def __init(self,
               id,
               title,
               release_date,
               country,
               genre,
               plot,
               budget,
               rating):
        self.id = id
        self.title = title
        if isinstance(release_date, str) is False:
            raise TypeError("Release date must be a string")
        if release_date[3] != "/":
            raise ValueError("Wrong format for film")
        # ...
        self.release_date = release_date
        self.country = country
        self.genre = genre
        self.plot = plot
        self.budget = budget
        if not isinstance(rating, Rating):
            raise TypeError("rating must be a rating")
        self.rating = rating
