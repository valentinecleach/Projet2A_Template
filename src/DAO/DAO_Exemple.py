import psycopg2
from getpass import getpass

# Demande d'ID utilisateur et mot de passe
user = input("Entrer votre identifiant : ") # mon id c'est id2464


# Connexion à la base de données
conn = psycopg2.connect(
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