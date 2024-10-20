from datetime import datetime
from typing import List  # , Optional

from DAO.db_connection import DBConnection, Singleton
from DAO.user_dao import UserDao
from Model.connected_user import ConnectedUser
from Model.movie import Movie
from Model.movie_collection import MovieCollection
