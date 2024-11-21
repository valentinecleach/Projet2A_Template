import pytest
from unittest import mock
from src.DAO.db_connection import DBConnector
from src.DAO.tables_creation import TablesCreation  # Importer le module contenant TablesCreation


@pytest.fixture
def mock_db_connection():
    """Fixture pour mocker la connexion à la base de données."""
    db_connector = mock.MagicMock(spec=DBConnector)
    yield db_connector


def normalize_sql_query(query):
    """Normalise une requête SQL pour enlever les espaces et les retours à la ligne."""
    return " ".join(query.strip().split())

def test_create_tables(mock_db_connection):
    """Test la création des tables dans la base de données."""
    
    # Mock de la méthode sql_query pour vérifier les appels à SQL
    mock_db_connection.sql_query = mock.MagicMock()

    # Création de l'instance de TablesCreation avec la connexion mockée
    tables_creation = TablesCreation(db_connection=mock_db_connection)

    # Les requêtes de création des tables que nous attendons
    create_queries = [
        """
        CREATE TABLE IF NOT EXISTS genre (
            id_genre INTEGER PRIMARY KEY,
            name_genre VARCHAR(255) NOT NULL
        );
        """,
        """
        "CREATE TABLE IF NOT EXISTS movie",
        "CREATE TABLE IF NOT EXISTS movie_collection",
        "CREATE TABLE IF NOT EXISTS link_movie_movie_collection",
        "CREATE TABLE IF NOT EXISTS link_movie_genre",
        "CREATE TABLE IF NOT EXISTS users",
        "CREATE TABLE IF NOT EXISTS comment",
        "CREATE TABLE IF NOT EXISTS follower",
        "CREATE TABLE IF NOT EXISTS user_movie_collection",
        "CREATE TABLE IF NOT NOT EXISTS movie_maker",
        "CREATE TABLE IF NOT EXISTS KnownFor",
        "CREATE TABLE IF NOT EXISTS rating"
    """
    ]

    # Normalisation des requêtes SQL avant de les comparer
    normalized_queries = [normalize_sql_query(q) for q in create_queries]

    # Vérifier que sql_query a bien été appelée pour chaque requête
    for query in normalized_queries:
        mock_db_connection.sql_query.assert_any_call(query)

    # Vérifier que sql_query a été appelée exactement le bon nombre de fois
    assert mock_db_connection.sql_query.call_count == len(create_queries)

    # Vérifier si le message 'All tables created successfully.' est bien affiché
    tables_creation.create_tables()  # Reappel de la méthode pour afficher ce message
    mock_db_connection.sql_query.assert_called_with(normalized_queries[-1])  # Vérifie l'appel de la dernière requête
