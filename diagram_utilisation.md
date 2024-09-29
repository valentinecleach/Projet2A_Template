```plantuml
@startuml
left to right direction

actor "Connecté" as c
actor "non connecté" as nc
'actor "professionnel" as pro
'actor "administrateur" as admin


rectangle Réseau_social_ciné{
  usecase "Se connecter" as 1
  usecase "Supprimer son compte" as 2
  usecase "Se deconnecter" as 3
  usecase "Rechercher des films" as 4
  usecase "Creer un compte" as 6
  usecase "Attribuer une note" as 7
  usecase "Obtenir des informations sur un film" as 8
  usecase "Ajouter à sa liste d'éclaireur" as 9
  usecase "Consulter sa collection de film" as 10
  usecase "Consulter un film" as 10b
  usecase "Rechercher des utilisateurs" as 11
  usecase "Obtenir leurs informations" as 11b
  usecase "Consulter leur collection de films" as 11c
  usecase "commenter ce film" as 12
  usecase "supprimer un film de sa collection" as 13
  usecase "ajouter à sa collection" as 13b
  usecase "Rechercher un acteur ou un réalisateur" as 14
  usecase "obtenir leurs informations" as 15
  usecase "Consulter sa liste d'éclaireurs" as 16
  usecase "supprimer un utilisateur de sa liste" as 16b
  usecase "Filtrer la liste des films" as 17
  


}
nc <|- c
'pro <|- admin


nc --> 6
nc --> 4
nc --> 1
nc --> 14

14 ..> 15


c --> 2
c --> 10
c --> 3
c --> 11
c --> 10b
c --> 16
c --> 17

11 ..> 9
10b ..> 7
10b ..> 12
10 ..> 13
10b ..> 13b
16 ..> 16b

4 ..> 8
'9 ..> 10

11 ..> 11b
11 ..> 11c
@enduml
