```plantuml

@startuml

left to right direction
package Ciné_film{
actor "Connecté" as c
actor "non connecté" as nc
}

rectangle Réseau_social_ciné{
  usecase "Se connecter" as 1
  usecase "S'authentifier" as 2
  usecase "Se deconnecter" as 3
  usecase "Rechercher des films" as 4
  usecase "Creer un compte" as 6
  usecase "Attribuer une note sur 10" as 7
  usecase "Obtenir des informations sur un film" as 8
  usecase "Ajouter un éclaireur" as 9
  usecase "Consulter collection" as 10


}
c --|> nc
nc --> 1
nc --> 4
nc --> 6
c --> 7
c --> 3
c --> 9
c --> 2
4 ..> 8
9 ..> 10




@enduml