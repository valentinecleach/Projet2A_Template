from dotenv import load_dotenv

from src.DAO.db_connection import DBConnection
from src.DAO.user_dao import UserDao
from src.Service.jwt_service import JwtService
from src.Service.user_service import UserService

load_dotenv()
db_connection = DBConnection()
user_dao = UserDao(db_connection)
jwt_service = JwtService()
user_service = UserService(user_dao)