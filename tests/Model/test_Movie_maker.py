import pytest
from src.Model.movie_maker import MovieMaker
from tests.conftest import james_cameron,avatar

@pytest.mark.parametrize(
    'kwargs, erreur, message_erreur',
    [
        ({'id_movie_maker': -1}, ValueError, "id_movie_maker must be a positive integer."),
        ({'adult': True}, ValueError, "adult must be False."),
        ({'name': ""}, ValueError, "name must be a non-empty string."),
        ({'biography': None}, ValueError, "biography must be a string."),
        ({'birthday': "invalid-date"}, ValueError, "birthday must be in the format YYYY-MM-DD."),
        ({'place_of_birth': None}, ValueError, "place_of_birth must be a string."),
        ({'deathday': "invalid-date"}, ValueError, "deathday must be empty or in the format YYYY-MM-DD."),
        ({'known_for_department': 123}, ValueError, "known_for_department must be a string."),
        ({'popularity': -5.0}, ValueError, "popularity must be a positive float."),
        ({'known_for': "not_a_list"}, TypeError, "known_for must be a list."),
        ({'known_for': [avatar,3]}, ValueError, "known_for must be a list of Movie objects."),
    ]
)

def test_movie_maker_init_echec(james_cameron, kwargs, erreur, message_erreur):
    # Mettre à jour james_cameron avec les arguments testés
    test_kwargs = james_cameron.copy()  # Créer une copie pour éviter de modifier la fixture
    test_kwargs.update(kwargs)  # Mettre à jour avec les arguments invalides
    with pytest.raises(erreur, match=message_erreur):
        MovieMaker(**test_kwargs)