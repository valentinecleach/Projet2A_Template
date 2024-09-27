import re
from datetime import datetime
# mettre en anglais

class MovieMaker :    
    def __init__(self, id_movie_maker: int, adult: bool, name: str, gender : int, biography: str, birthday: str, 
                    place_of_birth: str, deathday: str, know_for_department: str, popularity: float):
        """
        Initialise un nouvel objet MovieMaker avec les informations fournies.

        Paramètres:
        -----------
        id_movie_maker : int
            Identifiant TMDB unique de la personne.
        adult : bool
            Indique si la personne fait du contenu pour adulte
        name : str
            Nom de la personne.
        gender : int
            Indique le sexe de la personne (2 : homme)
        biography : str
            Biographie de la personne.
        birthday : str
            Date de naissance (format YYYY-MM-DD).
        place_of_birth : str
            Lieu de naissance.
        deathday : str
            Date de décès (format YYYY-MM-DD) ou None.
        know_for_department : str
            Département principal de la personne.
        popularity : float
            Score de popularité.
        """

        if not isinstance(id_movie_maker, int) or id_movie_maker < 0:
            raise ValueError("id_maker doit être un entier positif.")
        
        if adult is not False :
            raise ValueError("adult doit valoir false. Nous n")
        
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("name doit être une chaîne de caractères non vide.")
        
        if not isinstance(biography, str):
            raise ValueError("biography doit être une chaîne de caractères.")
        
        # Validation de la date de naissance (format YYYY-MM-DD)
        if not self._is_valid_date(birthday):
            raise ValueError("birthday doit être au format YYYY-MM-DD.")
        
        if not isinstance(place_of_birth, str):
            raise ValueError("place_of_birth doit être une chaîne de caractères.")
        
        # Validation de la date de décès (vide ou au format YYYY-MM-DD)
        if deathday and not self._is_valid_date(deathday):
            raise ValueError("deathday doit être vide ou au format YYYY-MM-DD.")
        
        if not isinstance(know_for_department, str):
            raise ValueError("know_for_department doit être une chaîne de caractères.")
        
        if not isinstance(popularity, float) or popularity < 0:
            raise ValueError("popularity doit être un nombre décimal positif.")
        
            self.id_movie_maker = id_movie_maker
            self.adult = adult
            self.name = name
            self.gender = gender
            self.biography = biography
            self.birthday = birthday
            self.place_of_birth = place_of_birth
            self.deathday = deathday
            self.know_for_department = know_for_department
            self.popularity = popularity