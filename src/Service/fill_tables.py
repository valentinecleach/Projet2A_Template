import random
from typing import Optional

from faker import Faker

from src.DAO.db_connection import DBConnector
from src.DAO.tables_creation import TablesCreation
from src.Service.movie_maker_service import MovieMakerService
from src.Service.movie_service import MovieService
from src.Service.user_interactions_service import UserInteractionService
from src.Service.user_movie_service import UserMovieService
from src.Service.user_service import UserService


class Fill_tables:
    """ file to fill the database

    Attributes
    ----------
    db_connection: DBConnector
        A connector to a database
    user_service: UserService
        user authentication
    movie_service: MovieService
        way to find a film   
    user_interaction_service: UserInteractionService
        interactivity between users 
    user_movie_service: UserMovieService
        users actions on movie page
    movie_maker_service: MovieMakerService
        way to found a moviemaker
    """
    
    def __init__(self, db_connection : DBConnector):
        """Constructor"""
        self.db_connection = db_connection
        self.user_service = UserService(db_connection)
        self.movie_service = MovieService(db_connection)
        self.user_interaction_service = UserInteractionService(db_connection)
        self.user_movie_service = UserMovieService(db_connection)
        self.movie_maker_service = MovieMakerService(db_connection)

    def fill_table_user(self, n : int):
        """ creation of a new users 

        Parameters
        ----------
        n : int 
            number of new users
        """ 

        fake = Faker()
        genders = [1, 2]  # 1 pour masculin, 2 pour féminin
        id_user_created = []
        for k in range(n):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            while len(username) < 5:
                username = fake.user_name()
            password = fake.password(length=12)
            gender = random.choice(genders)
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)  # Age between 18 and 80 
            email_address = fake.email()
            phone_number = None
            connected_user = self.user_service.sign_up(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                gender=gender,
                date_of_birth=date_of_birth,
                email_address=email_address,
                phone_number=phone_number
            )
            if connected_user:
                id_user_created.append(connected_user.id_user)
        print(f"Approximatively {n} user succesfully created.")
        return id_user_created

    def fill_table_movie(self,start_id, n):
        """ creation of new movies

        Parameters
        ----------
        n : int 
            number of newmovies
        """ 
        id_movie_created = []
        for k in range(start_id, start_id + n):
            movie =  self.movie_service.get_movie_by_id(k) 
            if movie: 
                id_movie_created.append(movie.id_movie)
        return id_movie_created

    def fill_table_movie_maker(self):
        """ creation of a new movies makers

        Parameters
        ----------
        n : int 
            number of new movies makers
        """ 
        movie_makers = [
            "Steven Spielberg", "Martin Scorsese", "Quentin Tarantino", "Christopher Nolan",
            "James Cameron", "Stanley Kubrick","Alfred Hitchcock","Francis Ford Coppola",
            "Ridley Scott","Tim Burton",
            "Woody Allen","George Lucas", "Ingmar Bergman", "Akira Kurosawa", "Hayao Miyazaki",
            "Catherine Bigelow","The Coen Brothers","David Fincher","Peter Jackson",
            "Clint Eastwood","Wes Anderson","Roman Polanski","Oliver Stone","Spike Lee","Fellini Federico",
            "Lars von Trier", "Jean-Luc Godard", "Krzysztof Kieslowski", "Bong Joon-ho", "Greta Gerwig"
        ]
        for movie_maker in movie_makers:
            movie_maker =  self.movie_maker_service.get_movie_maker_by_name(movie_maker) 

    def fill_table_follower(self, id_user_created, id_user_test : Optional[int] = None):
        if id_user_test:
            for k in range(10):
                id_followed = random.choice(id_user_created)
                while id_followed == id_user_test:
                    id_followed = random.choice(id_user_created)
                self.user_interaction_service.follow_user(id_user_test, id_followed)
        else:
            for id_user in id_user_created:
                for k in range(2): # we add max 2 link per user. Less if 2 time the same link
                    id_followed = random.choice(id_user_created)
                    while id_followed == id_user:
                        id_followed = random.choice(id_user_created)
                    self.user_interaction_service.follow_user(id_user, id_followed)

    def fill_table_favorite(self, id_user_created, id_movie_created, id_user_test : Optional[int] = None):
        if id_user_test :
            for k in range(10): 
                id_favorite_movie = random.choice(id_movie_created)
                self.user_interaction_service.add_favorite(id_user_test, id_favorite_movie)
        else:
            for id_user in id_user_created:
                for k in range(2): 
                    id_favorite_movie = random.choice(id_movie_created)
                    self.user_interaction_service.add_favorite(id_user, id_favorite_movie)

    def fill_table_rating(self, id_user_created, id_movie_created, id_user_test : Optional[int] = None):
        if id_user_test:
            for k in range(10):
                rating = random.randint(0,10)
                id_movie = random.choice(id_movie_created)
                self.user_movie_service.rate_film_or_update(id_user_test, id_movie, rating)
        else:
            for id_user in id_user_created:
                for k in range(2): 
                    rating = random.randint(0,10)
                    id_movie = random.choice(id_movie_created)
                    self.user_movie_service.rate_film_or_update(id_user, id_movie, rating)


    def fill_table_comment(self, id_user_created, id_movie_created, id_user_test : Optional[int] = None):
        movie_comments = [
            "The storyline was really engaging, I couldn't take my eyes off the screen!",
            "The acting was top-notch, especially the lead actor.",
            "The plot had some twists that I did not see coming, which made it even more exciting.",
            "I loved the cinematography, the visuals were absolutely stunning.",
            "The soundtrack really added to the atmosphere of the movie.",
            "The pacing was a bit slow at times, but the ending made up for it.",
            "The movie had great character development; I really cared about what happened to them.",
            "I was a bit disappointed by the ending, it felt rushed and unresolved.",
            "The humor in this film was spot-on; it made me laugh out loud multiple times.",
            "The action scenes were intense, but sometimes hard to follow due to the quick cuts."
        ]
        if id_user_test:
            for k in range(10): 
                comment = random.choice(movie_comments)
                id_movie = random.choice(id_movie_created)
                self.user_movie_service.add_or_update_comment(id_user_test, id_movie, comment)
        else:
            for id_user in id_user_created:
                for k in range(2): 
                    comment = random.choice(movie_comments)
                    id_movie = random.choice(id_movie_created)
                    self.user_movie_service.add_or_update_comment(id_user, id_movie, comment)

    def fill_the_database(self):
        Faker.seed(1234) # to fix seed. Same fake user each time to simplify testing
        random.seed(1234)
        id_user_created = self.fill_table_user(100)
        id_movie_created = self.fill_table_movie(100, 100)
        self.fill_table_follower(id_user_created)
        self.fill_table_favorite(id_user_created, id_movie_created)
        self.fill_table_rating(id_user_created, id_movie_created)
        self.fill_table_comment(id_user_created, id_movie_created)
        self.fill_table_movie_maker()
        ### Ajout de notre utilisateur de test :
        connected_user = self.user_service.sign_up(
                first_name="user_nocode",
                last_name="user_nocode",
                username="user_nocode",
                password="user_nocode123",
                gender = 1,
                date_of_birth="2024-11-22",
                email_address="nocode@gmail.com",
                phone_number="0707070707"
            )
        id_connected_user = connected_user.id_user
        self.fill_table_follower(id_user_created, id_user_test = id_connected_user)
        self.fill_table_favorite(id_user_created, id_movie_created,id_user_test = id_connected_user)
        self.fill_table_rating(id_user_created, id_movie_created,id_user_test = id_connected_user)
        self.fill_table_comment(id_user_created, id_movie_created,id_user_test = id_connected_user)

        print("Database successfully filled.")


##### To fill schema (take less than 5 min) ########

# db_connection = DBConnector()
# creation_object = TablesCreation(db_connection)
# my_object = Fill_tables(db_connection)
# my_object.fill_the_database()