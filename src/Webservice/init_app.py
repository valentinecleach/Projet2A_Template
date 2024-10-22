from dotenv import load_dotenv

from src.DAO.db_connection import DBConnection
from src.DAO.user_dao import UserDao
from src.Service.jwt_service import JwtService
from src.Service.user_service import UserService

load_dotenv()
db_connector = DBConnector()
user_repo = UserRepo(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)