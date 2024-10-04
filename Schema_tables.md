<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: Modèle Conceptuel des données CINEMAGIX
---
classDiagram

namespace Users {
class User{
    id_user [PK]: int 
    name : str
    phone_number : str
    email_address :UNIQUE NOT NULL :str 
    gender : int
    birthday : str
    password : str

 }
  class MovieCollection{
    id_user [FK]
    id_Movie [FK]
 }
 class Follower{
    id_user [FK]
    id_user_followed [FK]
    date : date
 }

class RatingComment{
    id_user [FK]: int
    id_movie [FK]: int
    comment : str
    rating: int or NA
    date: date
 }

}
namespace film {
class Movie{
    id_movie [PK]: int
    title : str
    adult : bool = false
    belongs_to_collection : dict
    budget : float
    origine_country : list
    original_language : str
    original_title : str
    overview : str
    popularity : float
    release_date : str
    revenue : int
    runtime : int
    vote_average : float
    vote_count : int
    tagline : str
    status : str

 }
class MovieGenre{
     id_movie [FK]
     id_genre [FK]
     }
 class Genre{
    id_genre [PK]: int
    genre_name : str
 }
}
namespace maker{
class MovieMaker{
    id_maker  [PK]: int
    imdb_id : str
    adult : bool = false
    name : str
    gender : int
    biography : str
    birthday : str
    place_of_birth : str
    deathday : str
    known_for_department : str
    popularity : float
 }
 class KnownFor{
    id_maker [FK]
    id_movie [FK]
 }
}

User --> RatingComment
User -- Follower
RatingComment --> Movie
User --> MovieCollection
MovieCollection --> Movie
MovieMaker --> KnownFor
KnownFor --> Movie
Movie --> MovieGenre
MovieGenre --> Genre
