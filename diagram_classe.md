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

   +log_out()
   
 }
class NonConnectedUser{
    +sign_up(): ConnectedUser:
    +search_movie(movie : str)
    +log_in(id : str, password : str)
    +find_user(user : str)
 }

%% UserService
class UserService{
    +find_user(name : str  )
    +view_user_collection(id_user : int)
    +follow(user : User)
    +unfollow(user : User)
    +add_movie(film : Movie)
    +rate(film : Movie, rating : int)
    +add_comment(film : Movie, comment : str)
    +sign_up(): ConnectedUser:
    +log_in(id : str, password : str)
    +delete_account()
 }
class UserDao{
    +find_user(name : str  )
    +view_user_collection(id_user : int)
    +follow(user : User)
    +unfollow(user : User)
    +add_movie(film : Movie)
    +rate(film : Movie, rating : int)
    +add_comment(film : Movie, comment : str)
    +sign_up(): ConnectedUser:
    +log_in(id : str, password : str)
    +delete_account()
 }
class RatingComment{
    +id_user : int
    +id_movie : int
    +comment : str
    +rating: int or NA
    +check_comment() 
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


class TMDBConnector{
    +find_movie(movie : str  )
    +view_comments(movie : str)
    +filter_by_genre(genre : int)
    +filter_by_popularity()

    +find_movie_maker(movie : str  )
 }

%% MovieService
class MovieService{
    +find_movie(movie : str  )
    +view_comments(movie : str)
    +filter_by_genre(genre : int)
    +filter_by_popularity()
    +find_movie_maker(maker : str  )
 }
class MovieDao{
    +find_movie(movie : str  )
    +view_comments(movie : str)
    +filter_by_genre(genre : int)
    +filter_by_popularity()
    +find_movie_maker(maker : str  )
  }



TMDBConnector >.. MovieService
ConnectedUser --|> NonConnectedUser : Extends
ConnectedUser "1" --> "*" RatingComment : Comment or rate
ConnectedUser --> UserService 
UserService ..> UserDao

Movie "1" <-- "*" RatingComment
MovieMaker "1..*" --* "*" Movie
ConnectedUser "*" --> "*" ConnectedUser : follow
ConnectedUser "*" --> "*" Movie : collect
Movie "1..*" --> "1..*" Genre

Movie --> MovieService 
MovieService ..> MovieDao
