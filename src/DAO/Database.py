import psycopg2
from getpass import getpass

class Database:
    def __init__(self):
        try :
            self.connexion = psycopg2.connect(
                dbname = "id2464",
                user = "id2464",
                password = "id2464",
                host = "sgbd-eleves.domensai.ecole",
                port = "5432"
            )
        except psycopg2.DatabaseError as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            

# sert à modifier la table de données
    def execute_query(self, query : str, data = None):
        try:
            with self.connexion.cursor() as cursor : # with contient le cursor.close
                cursor.execute(query, data)
                self.connexion.commit()
        except psycopg2.DatabaseError as e:
            print(f"Erreur lors de l'execution de la requête :{e}")
            self.connexion.rollback() # permet d'annuler les modifs en cas d'erreur
        

# récupérer des données depuis la base (renvoie la première ligne du résultat)
    def fetch_one(self, query, data= None):
        try :
            with self.connexion.cursor() as cursor :
                cursor.execute(query, data)
                return cursor.fetchone()
        except psycopg2.DatabaseError as e: 
            print(f"Erreur lors de la récupération des données : {e}")
        

# terminer la connexion 
    def close(self):
        try:
            self.conn.close()
        except psycopg2.DatabaseError as e:
            print(f"Erreur lors de la fermeture de la connexion : {e}")

# Connexion à la base de données

conn = Database(
    dbname=user,
    user=user,
    password=user,
    host="sgbd-eleves.domensai.ecole",
    port="5432"
)

# Créer un curseur
cursor = conn.cursor()

# Utiliser ton schéma pour la session
cursor.execute("SET search_path TO projet_info;")

# Exemple de création de table dans ton schéma
cursor.execute("""
CREATE TABLE exemple (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50),
    description TEXT
);
""")

# Confirmer la transaction
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()


# ca foctionne bien, j'ai créé une table exemple dans le schéma projet_info