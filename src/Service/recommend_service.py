from src.DAO.db_connection import DBConnector
from src.DAO.recommend_dao import RecommendDao


class RecommendService:
    """An object to recommend users to follow and movies to the users

    Attributes
    ----------
    db_connection : DBConnector
        A connector to a database
    """
    def __init__(self, db_connection: DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.recommend_dao = RecommendDao(db_connection)

    def find_users_to_follow(self, id_user: int):
        """
        Finds users to follow for a given user.

        Parameters
        ----------
        id_user: int
            User ID for which to find follow recommendations.

        Returns
        -------
        list[User] | None
            A list of recommended users to follow or popular users if no recommendations are found.
            If neither are possible or if the users id isn't entered, the function will return None.
        """
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

    def find_movie_to_collect(self, id_user: int, filter: dict = {}):
        """
        Finds movies to collect for a given user given a filter. 
        If the recommendation algorithm doesn't find any movies, it recommends according to the popularity index.

        Parameters
        ----------
        id_user : int
            User ID for whom to find movie recommendations.
        filter : dict
            A dictionary that gives a filter for the movie. For example {"genre" : "drama"}

        Returns
        -------
        list[Movie] | None
            Returns a list of movies that correspond to the filter.
            If no movies can be found, then the method returns None.
        """
        if not id_user:
            print("User ID is required")
            return None
        movies = self.recommend_dao.recommend_movies(id_user, filter)
        if movies:
            return movies
        else:
            popular = self.recommend_dao.get_popular_movies(filter)
            if popular:
                return popular
            else:
                print("No movies found at the moment:")
                return None


# db_connection = DBConnector()
# # # # # # # u = UserDao(db_connection)
# service = RecommendService(db_connection)
# print(service.find_users_to_follow(431))
# print(service.find_movie_to_collect(224,{"name_genre" : 'drama'}))
# date_of_birth = user.date_of_birth
# print(isinstance(date_of_birth, date))
# python src/Service/recommend_service.py
