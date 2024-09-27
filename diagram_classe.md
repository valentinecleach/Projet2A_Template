<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

title: Cine & Films
---

```mermaid
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
   +rate(film : Film, rating : Rating_Comment)
   +add_comment(film : Film, comment : Rating_Comment)
   +log_out()
   +delete_account()
 }
}
class Movie{
    +id : int
    +title : str
    +adult : bool = false
    +belongs_to_collection : dict
    +budget : float
    +genre : list[dict]
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
class MovieMaker{
    +id : int
    +imdb_id : str
    +adult : bool = false
    +name : str
    +biography : str
    +birthday : str
    +place_of_birth : str
    +deathday : str
    +known_for_department : str
    +popularity : float
    +known_for : list[Movie]
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
