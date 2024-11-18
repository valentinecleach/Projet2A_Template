from dotenv import load_dotenv

from src.DAO.db_connection import DBConnector
from src.DAO.movie_dao import MovieDAO
from src.DAO.user_dao import UserDao
from src.DAO.user_follow_dao import UserFollowDao
from src.Service.jwt_service import JwtService
from src.Service.movie_maker_service import MovieMakerService
from src.Service.movie_service import MovieService
from src.Service.user_interactions_service import UserInteractionService
from src.Service.user_movie_service import UserMovieService
from src.Service.user_service import UserService
from src.Service.recommend_service import RecommendService

load_dotenv()
db_connection = DBConnector()
user_dao = UserDao(db_connection)
movie_dao = MovieDAO(db_connection)
user_follow_dao = UserFollowDao(db_connection)
jwt_service = JwtService()
user_service = UserService(db_connection)
movie_service = MovieService(db_connection)
movie_maker_service = MovieMakerService(db_connection)
user_interaction_service = UserInteractionService(db_connection)
user_movie_service = UserMovieService(db_connection)
