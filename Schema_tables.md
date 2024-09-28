<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: Cine & Films
---
classDiagram

namespace Users {
class User{
    +id_user : int
    +name : str
    +phone_number : str
    +email_address : str
    +gender : int
    +birthday : str
    +password : str

 }
  class MovieCollection{
    id_user
    id_Movie
 }
 class Follower{
    id_user
    id_user_followed
 }

class RatingComment{
    +id_user : int
    +id_movie : int
    +comment : str
    +rating: int or NA 
 }

}
class Movie{
    +id_movie : int
    id_genre
    +title : str
    +adult : bool = false
    +belongs_to_collection : dict
    +budget : float
    +genre : list[Genre]
    +origine_country : list
    +original_language : str
    +original_title : str
    +overview : str
    +popularity : float
    +release_date : str
    +revenue : int
    +runtime : int
    +vote_average : float
    +vote_count : int
    +tagline : str
    +status : str

 }
 class Genre{
    +id_genre : int
    +genre_name : str
 }
class MovieMaker{
    +id_maker : int
    +imdb_id : str
    +adult : bool = false
    +name : str
    +gender : int
    +biography : str
    +birthday : str
    +place_of_birth : str
    +deathday : str
    +known_for_department : str
    +popularity : float
 }
 class KnownFor{
    id_maker
    id_movie
 }

User --> RatingComment
User -- Follower
RatingComment --> Movie
User --> MovieCollection
MovieCollection --> Movie
MovieMaker --> KnownFor
KnownFor --> Movie
Movie --> Genre
