from src.DAO.db_connection import DBConnector
from src.Service.user_service import UserService
from src.Service.movie_service import MovieService
from src.Service.user_interactions_service import UserInteractionService
from src.Service.user_movie_service import UserMovieService
from src.DAO.tables_creation import TablesCreation
from src.Service.movie_maker_service import MovieMakerService
from faker import Faker
import random

class Fill_tables:
    def __init__(self, db_connection : DBConnector):
        self.db_connection = db_connection
        self.user_service = UserService(db_connection)
        self.movie_service = MovieService(db_connection)
        self.user_interaction_service = UserInteractionService(db_connection)
        self.user_movie_service = UserMovieService(db_connection)
        self.movie_maker_service = MovieMakerService(db_connection)

    def fill_table_user(self, n : int):
        fake = Faker()
        genders = [1, 2]  # 1 pour masculin, 2 pour féminin
        id_user_created = []
        
        # Générer 200 utilisateurs
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
        id_movie_created = []
        for k in range(start_id, start_id + n):
            movie =  self.movie_service.get_movie_by_id(k) 
            if movie: 
                id_movie_created.append(movie.id_movie)
        return id_movie_created

    def fill_table_movie_maker(self):
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

    def fill_table_follower(self, id_user_created):
        for id_user in id_user_created:
            for k in range(3): # we add max 3 link per user. Less if 2 time the same link
                id_followed = random.choice(id_user_created)
                while id_followed == id_user_created:
                    id_followed = random.choice(id_user_created)
                self.user_interaction_service.follow_user(id_user, id_followed)

    def fill_table_favorite(self, id_user_created, id_movie_created):
        for id_user in id_user_created:
            for k in range(3): # we add max 3 link per user. Less if 2 time the same link
                id_favorite_movie = random.choice(id_movie_created)
                self.user_interaction_service.add_favorite(id_user, id_favorite_movie)

    def fill_table_rating(self, id_user_created, id_movie_created):
        for id_user in id_user_created:
            for k in range(3): 
                rating = random.randint(0,10)
                id_movie = random.choice(id_movie_created)
                self.user_movie_service.rate_film_or_update(id_user, id_movie, rating)


    def fill_table_comment(self, id_user_created, id_movie_created):
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
        for id_user in id_user_created:
            for k in range(3): 
                comment = random.choice(movie_comments)
                id_movie = random.choice(id_movie_created)
                self.user_movie_service.add_or_update_comment(id_user, id_movie, comment)

    def fill_the_database(self):
        id_user_created = self.fill_table_user(100)
        id_movie_created = self.fill_table_movie(100, 100)
        self.fill_table_follower(id_user_created)
        self.fill_table_favorite(id_user_created, id_movie_created)
        self.fill_table_rating(id_user_created, id_movie_created)
        self.fill_table_comment(id_user_created, id_movie_created)
        self.fill_table_movie_maker()
        print("Database successfully filled.")


##### To fill schema (take less than 10 min) ########

# db_connection = DBConnector()
# creation_object = TablesCreation(db_connection)
# my_object = Fill_tables(db_connection)
# my_object.fill_the_database()