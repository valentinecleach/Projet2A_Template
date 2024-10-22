from dotenv import load_dotenv

from src.DAO.db_connection import DBConnection
from src.DAO.UserRepo import UserRepo
from src.Service.JWTService import JwtService
from src.Service.UserService import UserService

load_dotenv()
db_connector = DBConnector()
user_repo = UserRepo(db_connector)
jwt_service = JwtService()
user_service = UserService(user_repo)