<<<<<<< HEAD
```plantuml  
=======
```plantuml

>>>>>>> fa52feb3fa5a73dbc0211831548393bf978c2bc8
@startuml
left to right direction

actor "Connecté" as c
actor "non connecté" as nc
'actor "professionnel" as pro
'actor "administrateur" as admin


rectangle Réseau_social_ciné{
  usecase "Se connecter" as 1
  usecase "Supprimer mon compte" as 2
  usecase "Se deconnecter" as 3
  usecase "Rechercher des films" as 4
  usecase "Creer un compte" as 6
  usecase "Attribuer une note sur 10 à un film" as 7
  usecase "modifier ou effacer ma note" as 7b
  usecase "Obtenir des informations sur un film" as 8
  usecase "Ajouter/ supprimer un utilisateur à sa liste d'éclaireur" as 9
  'usecase "Consulter collection" as 10
  usecase "Rechercher des utilisateurs" as 11
  usecase "Obtenir des informations sur un utilisateur" as 11b
  usecase "Consulter sa collection de films" as 11c
  


}
nc <|- c
'c <|- pro
'pro <|- admin

nc --> 1
nc --> 4
nc --> 6
nc --> 11


c --> 7
c --> 3
c --> 9
c --> 2

4 ..> 8
7 ..> 7b

11 ..> 11b
11b ..> 11c
@enduml
