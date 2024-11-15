from src.DAO.db_connection import DBConnector
from src.Service.user_interactions_service import UserInteractionService


def test_search_user_found():
    """
    Test de la recherche d'un utilisateur.
    Cette fonction cherche un utilisateur qui existe et vérifie si l'utilisateur est bien retrouvé.
    """
    db_connection = (
        DBConnector()
    )  # Assurez-vous que DBConnector est correctement initialisé
    user_interaction_service = UserInteractionService(db_connection)

    result = user_interaction_service.search_user("user001")
    print(result)  # Affiche le résultat pour vérifier la recherche d'utilisateur
    assert result is not None  # Vérifie que l'utilisateur est trouvé


def test_search_user_not_found():
    """
    Test de la recherche d'un utilisateur qui n'existe pas.
    Cette fonction cherche un utilisateur qui n'existe pas et vérifie si la recherche échoue.
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

    # Étape 2: L'utilisateur 1 annule son suivi de l'utilisateur 2
    user_service.unfollow_user(follower_id, followee_id)
    print(
        f"User {follower_id} is no longer following {followee_id}"
    )  # Vérification de l'annulation du suivi

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
