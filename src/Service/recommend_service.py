from src.DAO.db_connection import DBConnector
from src.DAO.recommend_dao import RecommendDao


class RecommendService:
    def __init__(self, db_connection: DBConnector):
        """
        Initializes the recommendation service with a database connection.

        :param db_connection: Instance of DBConnector for database connection.
        """
        self.db_connection = db_connection
        self.recommend_dao = RecommendDao(db_connection)

    def find_users_to_follow(self, id_user: int):
        """
        Finds users to follow for a given user.

        :param id_user: User ID for whom to find follow recommendations.
        :return: List of recommended users to follow or popular users if no recommendations are found.
        """
        if not id_user:
            print("User ID is required")
            return None
        users = self.recommend_dao.recommend_users_to_follow(id_user)
        if users:
            return users
        else:
            popular = self.recommend_dao.get_popular_users(id_user)
            if popular:
                return popular
            else:
                print("No users found at the moment:")
                return None

    def find_movie_to_collect(self, id_user: int,, filter: dict = {}):
        """
        Finds movies to collect for a given user.

        :param id_user: User ID for whom to find movie recommendations.
        :return: List of recommended movies to collect or popular movies if no recommendations are found.
        """
        if not id_user:
            print("User ID is required")
            return None
        movies = self.recommend_dao.recommend_movies(id_user,filter)
        if movies:
            return movies
        else:
            popular = self.recommend_dao.get_popular_movies(id_user,filter)
            if popular:
                return popular
            else:
                print("No movies found at the moment:")
                return None


# db_connection = DBConnector()
# # # # # u = UserDao(db_connection)
# service = RecommendService(db_connection)
# # # print(len(service.find_users_to_follow(24)))
# print(service.find_movie_to_collect(224))
# date_of_birth = user.date_of_birth
# print(isinstance(date_of_birth, date))
# python src/Service/recommend_service.py
