<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->


```mermaid
---
title: Cine & Films
---
classDiagram

namespace Users {
class ConnectedUser{
    +id_user : int
    +name : str
    +phone_number : str
    +email_address : str
    +gender : int
    +birthday : str
    +password : str

   +follow(user : User)
   +unfollow(user : User)
   +add_film(film : Film)
   +rate(film : Film, rating : int)
   +add_comment(film : Film, comment : str)
   +log_out()
   +delete_account()
 }
class NonConnectedUser{
    +sign_up(): ConnectedUser:
    +search_movie(movie : str)
    +log_in(id : str, password : str)
    +search_user(user : str)
 }
}
class Movie{
    +id_movie : int
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
    +nbr_ratings() : int
    +overall_rating() : float

 }
 class Genre{
    +id : int
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
class RatingComment{
    +id_user : int
    +id_movie : int
    +comment : str
    +rating: int or NA
    
 }

class TMDBConnector{
    +search_movie(movie : str)
 }


class MovieService{
    +search_movie(movie : str  )
 }
class MovieDao{
    +search_movie(movie : str)
 }






ConnectedUser --|> NonConnectedUser : Extends
ConnectedUser "1" --> "*" RatingComment : Comment or rate
Movie "1" <-- "*" RatingComment
MovieMaker "1..*" --* "*" Movie
ConnectedUser "*" --> "*" ConnectedUser : follow
ConnectedUser "*" --> "*" Movie : collect
Movie "1..*" --> "1..*" Genre
Movie -- MovieService 
MovieService-- MovieDao
TMDBConnector -- MovieService








