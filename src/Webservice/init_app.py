from dotenv import load_dotenv

from src.DAO.db_connection import DBConnector
from src.DAO.user_dao import UserDao
from src.DAO.movie_dao import MovieDAO
from src.Service.jwt_service import JwtService
from src.Service.user_service import UserService
from src.Service.movie_service import MovieService

load_dotenv()
db_connection = DBConnector()
user_dao = UserDao(db_connection)
movie_dao = MovieDAO(db_connection)
jwt_service = JwtService()
user_service = UserService(db_connection)
movie_service = MovieService(db_connection)