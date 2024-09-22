%% code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax
---
title: Cine & Films
---
classDiagram
namespace Users {
class NonConnectedUser{
    +sign_up(): ConnectedUser:
    +search_film(film : str)
    +log_in(id : str, password : str)
    +search_user(user : str)
 }

class ConnectedUser{
    +name : str
    +phone_number : str
    +email_address : str
    +date_of_birth : str
    +password : str
    +id : str
    +film_collection : list
    +scout_list : list

   +follow(user : User)
   +unfollow(user : User)
   +add_film(film : Film)
   +rate(film : Film, rating : int)
   +add_comment(film : Film, comment : str)
   +log_out()
   +delete_account()    
 }
}
class Movie{
    +title : str  
    +release_date : str 
    +country : str
    +duration : int
    +genre : str
    +plot : str
    +budget :  float
    +rating : MovieRating
    +filmmaker : list[MovieMaker]
 }
class MovieMaker{
    +name : str
    +date_of_birth : str
    +country : str
    +type : str
 }
class MovieRating{
    +name : str
    +all_ratings : list[Rating_Comment]
    +nbr_ratings() : int
    +overall_rating() : float
 }
class Rating_Comment{
    +comment : str
    +rating: int or NA
    +who_rated : ConnectedUser
 }
MovieRating --o Movie
Rating_Comment --o MovieRating
MovieMaker "*" --* "*" Movie
ConnectedUser --|> NonConnectedUser : Extends



