from src.DAO.db_connection import DBConnector
from src.Service.user_interactions_service import UserInteractionService


def test_search_user_found():
    """
    Test de la recherche d'un utilisateur.
    Cette fonction cherche un utilisateur qui existe et vérifie
    si l'utilisateur est bien retrouvé.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    result = user_interaction_service.search_user("garrettmercer")
    print(result)
    assert result is not None  # Vérifie que l'utilisateur est trouvé


def test_search_user_not_found():
    """
    Test de la recherche d'un utilisateur qui n'existe pas.
    Cette fonction cherche un utilisateur qui n'existe pas
    et vérifie si la recherche échoue.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    result = user_interaction_service.search_user("unknownuser")
    print(result)  # Affiche le résultat, qui devrait être None
    assert result is None  # Vérifie que l'utilisateur n'est pas trouvé


def test_follow_user_success():
    """
    Test du suivi d'un utilisateur avec succès.
    Cette fonction permet à un utilisateur de suivre un autre utilisateur.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    follower_id = 1
    followee_id = 2
    user_interaction_service.follow_user(follower_id, followee_id)
    print(f"User {follower_id} is now following {followee_id}")  # Vérification du suivi
    # Aucun retour attendu si cela fonctionne bien


def test_follow_user_self_follow():
    """
    Test où un utilisateur essaie de se suivre lui-même. Cela devrait lever une exception.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    follower_id = 1
    followee_id = 1  # L'utilisateur essaie de se suivre lui-même
    try:
        user_interaction_service.follow_user(follower_id, followee_id)
    except ValueError as e:
        print(e)  # Attendu: "A user cannot follow themselves."
        assert (
            str(e) == "A user cannot follow themselves."
        )  # Vérifie que l'erreur attendue est levée


def test_unfollow_user_success():
    """
    Test de l'annulation du suivi d'un utilisateur avec succès.
    Cette fonction permet à un utilisateur d'arrêter de suivre un autre utilisateur.
    """
    # Initialisation de la connexion à la base de données
    db_connection = DBConnector()

    # Initialisation du service d'interaction utilisateur
    user_service = UserInteractionService(db_connection)

    # IDs des utilisateurs
    follower_id = 1
    followee_id = 2

    # Étape 1: L'utilisateur 1 suit l'utilisateur 2
    user_service.follow_user(follower_id, followee_id)

    # Étape 3: Tentative de désabonnement une deuxième fois (doit lever une exception)
    try:
        user_service.unfollow_user(follower_id, followee_id)
    except ValueError as e:
        print(e)  # Doit afficher "This user is not being followed."


def test_unfollow_user_not_following():
    """
    Test où un utilisateur essaie de se désabonner d'un utilisateur qu'il ne suit pas. Cela devrait lever une exception.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    follower_id = 1
    followee_id = 3  # L'utilisateur n'a pas suivi ce deuxième utilisateur
    try:
        user_interaction_service.unfollow_user(follower_id, followee_id)
    except ValueError as e:
        print(e)  # Attendu: "This user is not being followed."
        assert (
            str(e) == "This user is not being followed."
        )  # Vérifie que l'erreur attendue est levée


def test_add_favorite_success():
    """
    Test de l'ajout d'un film à la liste des favoris avec succès.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    user_id = 217
    movie_id = 19965
    user_interaction_service.add_favorite(user_id, movie_id)
    print(f"Movie {movie_id} added to User {user_id}'s favorites.")

    # Vérification si le film a bien été ajouté
    favorites = user_interaction_service.get_user_favorites(user_id)
    assert any(
        fav["id_movie"] == movie_id for fav in favorites
    ), "Le film n'a pas été ajouté aux favoris."


def test_add_favorite_duplicate():
    """
    Test où un utilisateur essaie d'ajouter un film déjà présent dans ses favoris.
    Cela devrait lever une exception.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    user_id = 1
    movie_id = 100
    user_interaction_service.add_favorite(user_id, movie_id)  # Premier ajout réussi
    try:
        user_interaction_service.add_favorite(user_id, movie_id)  # Deuxième ajout
    except ValueError as e:
        print(e)  # Attendu: "This movie is already in favorites."
        assert str(e) == "This movie is already in favorites."


def test_get_user_favorites():
    """
    Teste la récupération des favoris d'un utilisateur.
    """
    db_connection = DBConnector()
    user_interaction_service = UserInteractionService(db_connection)

    # ID de l'utilisateur
    user_id = 217

    # Ajouter deux films aux favoris
    user_interaction_service.add_favorite(user_id, 19965)
    user_interaction_service.add_favorite(user_id, 19995)

    # Récupérer les favoris
    favorites = user_interaction_service.get_user_favorites(user_id)
    print(f"Favorites for user {user_id}: {favorites}")

    # Vérifie que la liste contient les films ajoutés
    assert any(
        fav["id_movie"] == 19965 for fav in favorites
    ), "Le film 19965 n'est pas dans les favoris."
    assert any(
        fav["id_movie"] == 19995 for fav in favorites
    ), "Le film 29985 n'est pas dans les favoris."
