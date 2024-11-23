<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: CINEMAGIX
---
classDiagram

namespace Main {
class User{
    +ip_address: str }
class ConnectedUsed{
    +id_user : int
    +username: str
    + hashed_password: str
    +date_of_birth: date
    +gender: int
    +first_name: str
    +last_name: str
    +email_address: str
    +password_token: str
    +phone_number: s
+to_dict()
 }


class Comment{
    +user: ConnectedUser,
    +movie: Movie,
    +date: str,
    +comment: str,
 }
class Rating{
    +user: ConnectedUser,
    +movie: Movie,
    +date: str,
    +rating: int,
 }


class Movie{
    +id_movie : int
    +title : str
    +adult : bool = false
    +budget : float
    +origine_country : list[str]
    +original_language : str
    +original_title : str
    +overview : str
    +popularity : float
    +release_date : str
    +revenue : int
    +runtime : int
    +vote_average : float
    +vote_count : int
    +adult : bool=False

 }
 class MovieCollection{
    id: int
    name: str}
 class Genre{
    +id : int
    +genre_name : str
 }
class MovieMaker{
    +id_movie_maker : int
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
}
User <|-- ConnectedUsed
ConnectedUsed "1" --> "*" Comment : Comment a movie
ConnectedUsed "1" --> "*" Rating : Rate a movie


Movie "1" <-- "*" Comment
Movie "1" <-- "*" Rating
MovieMaker "1..*" --* "*" Movie : Known for
Movie "1..*" --* "*" MovieCollection : belongs to
ConnectedUsed "*" --> "*" ConnectedUsed : follow
ConnectedUsed "*" --> "*" Movie : collect
Movie "1..*" --* "1..*" Genre

  