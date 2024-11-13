<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
config:
  theme: default
title: Modèle Conceptuel des données CINEMAGIX
---
classDiagram
namespace MOVIE {
class movie {
            id_movie INTEGER [PK]
            title VARCHAR 255
            budget FLOAT
            origin_country VARCHAR 255
            original_language VARCHAR 255
            original_title VARCHAR 255 
            overview TEXT 
            popularity FLOAT 
            release_date DATE 
            revenue BIGINT 
            runtime INTEGER 
            vote_average FLOAT 
            vote_count INTEGER 
            adult BOOLEAN
        }

class genre {
            id_genre INTEGER [PK]
            name_genre VARCHAR 255
        }

class movie_collection {
            id_movie_collection INTEGER [PK]
            name_movie_collection VARCHAR 255
        }
class link_movie_movie_collection {
            id_movie INTEGER [FK]
            id_movie_collection INTEGER [FK]
}

class link_movie_genre {
            id_movie INTEGER [FK]
            id_genre INTEGER [FK]}

}
namespace MAKERS {
class movie_maker {
            id_movie_maker INTEGER [PK]
            adult BOOLEAN
            name VARCHAR 255
            gender INTEGER
            biography TEXT
            birthday DATE 
            place_of_birth VARCHAR 255 
            deathday DATE 
            known_for_department VARCHAR 255 
            popularity FLOAT 
            known_for JSONB
        }

class KnownFor{
            id_movie INTEGER [FK]
            id_movie_maker INTEGER [FK] }
}
namespace USERS{
class users {
            id_user SERIAL [PK]
            username VARCHAR 255 UNIQUE
            first_name VARCHAR 255
            last_name VARCHAR 255
            password_token VARCHAR 255
            hashed_password VARCHAR 255
            email_address VARCHAR 255 UNIQUE
            date_of_birth DATE
            phone_number VARCHAR 255
            gender INTEGER
        }

class rating {
            id_user INTEGER [FK]
            id_movie INTEGER [FK]
            rating INTEGER
            date VARCHAR 255}

class comment {
            id_user INTEGER [FK]
            id_movie INTEGER [FK]
            comment TEXT
            date DATE [FK]}

class follower {
            id_user INTEGER [FK]
            id_user_followed INTEGER [FK]
            date DATE}

%%class user_collection{
            %%id_user INTEGER [FK]
            %%id_collection INTEGER [FK]
            %%date DATE
%%}

class user_movie_collection {
            id_user INTEGER [FK] 
            id_movie INTEGER [FK]
            date DATE
}


}
users "1" --> "*" rating
users "1.*" --> "*" comment
users "*" -- "*" follower
comment "*"-->"1" movie
rating "*"-->"1" movie
users "1"-->"*" user_movie_collection
user_movie_collection"*" --> "1.*"movie
%%user_collection --> user_movie_collection
movie "1"-->"*" link_movie_movie_collection
link_movie_movie_collection"1.*" -->"1"movie_collection

movie_maker "1" --> "1.*"KnownFor
KnownFor"1.*" --> "1"movie
movie "1"-->"1.*" link_movie_genre
link_movie_genre"1.*" -->"1" genre

