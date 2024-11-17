from src.DAO.db_connection import DBConnector
from src.Service.user_service import UserService
from src.Service.movie_service import MovieService
from src.Service.user_interactions_service import UserInteractionService
from faker import Faker
import random

class Fill_tables:
    def __init__(self, db_connection : DBConnector):
        self.db_connection = db_connection
        self.user_service = UserService(db_connection)
        self.movie_service = MovieService(db_connection)
        self.user_interaction_service = UserInteractionService(db_connection)

    def fill_table_user(self, n : int):
        fake = Faker()
        genders = [1, 2]  # 1 pour masculin, 2 pour féminin
        
        # Générer 200 utilisateurs
        for _ in range(n):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            while len(username) < 5:
                username = fake.user_name()
            password = fake.password(length=12)
            gender = random.choice(genders)
            date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)  # Âge entre 18 et 80 ans
            email_address = fake.email()
            phone_number = None

            # Appeler la méthode `sign_up` pour insérer cet utilisateur dans la base de données
            self.user_service.sign_up(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                gender=gender,
                date_of_birth=date_of_birth,
                email_address=email_address,
                phone_number=phone_number
            )
        print(f"{n} utilisateurs ont été créés avec succès.")

    def fill_table_movie(self,start_id, n):
        for k in range(start_id, start_id + n):
            self.movie_service.get_movie_by_id(k)

    def fill_table_follower(self, n:int):
        self.user_interaction_service.follow_user(250,10000)
        for k in range(n):
            id_user = random.randint(250,350)
            id_followed = random.randint(250,350)
            self.user_interaction_service.follow_user(id_user, id_followed)

    def fill_table_favorite(self, n:int):
        for k in range(n):
            id_user = random.randint(250,350)
            id_favorite_moovie = random.randint(250,500)
            self.user_interaction_service.add_favorite(id_user, id_favorite_moovie)


#db_connection = DBConnector()
#my_object = Fill_tables(db_connection)
#my_object.fill_table_user(200)
#my_object.fill_table_movie(19900, 100)
#my_object.fill_table_follower(20)
#my_object.fill_table_favorite(250)