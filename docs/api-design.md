# lister tous les livres  
GET /livres  
**Body attendu** : aucun  
**reponse json**  :  
[  
 {
    "id" : 1,
    "titre" : "le romain",
    "auteur" : "Marie Elisabeth",
    "disponible" : true
 }, 

 {
     "id" : 2,
    "titre" : "les bois",
    "auteur" : "Marie dembele",
    "disponible" : false

 } 
]  

**Codes possibles** : 200 ok , 500 internal server error

# Consulter un livre  
GET /livres/{id}  

**Body attendu** : aucun  
**reponse json**  :  


 {
     "id" : 2,
    "titre" : "les bois",
    "auteur" : "Marie dembele",
    "disponible" : false

 } 


**Codes possibles** : 200 ok , 404 not found  

# Ajouter un livre  
POST /livres  

**Body attendu** :  
{
    "id" : 5,
    "titre" : "les bois2",
    "auteur" : "Marie dembele2",
    "annee" : 1963,
    "categories" : "sience"
}
**reponse json**  :  
 {
     "id" : 2,
    "message" : "livres ajouter avec success"

 } 


**Codes possibles** : 201 created , 400 bad request, 401 unhautorized  

# Modifier un livre  

PUT /livres/{id}  

**Body attendu** :  
{
    "annee" : 1980,
    "categories" : "sience"
}
**reponse json**  :  
 {
    "message" : "livre mise a jour"

 } 


**Codes possibles** : 200 ok , 400 bad request, 404 not found

# Supprimer un livre  
DELETE /livres/{id}  
**Body attendu** : aucun
**reponse json**  :  
 {
    "message" : "livre supprimer"

 } 


**Codes possibles** : 200 ok , 404 not found  
# Emprunter un livre  
POST /emprunts   
**Body attendu** :  
{
    "id_livres" : 2,  
    "id_adherent" : 10

}


**reponse json**  :  
 {
  "idEmprunt": 42,  
  "dateEmprunt": "2026-07-20",  
  "dateRetourPrevue": "2026-08-03"

 } 


**Codes possibles** : 201 created , 400 bad request, 404 not found, 409 conflicts  

# Retourner un livre  
PATCH /emprunts/{id}/retour  

**Body attendu** : aucun  

**reponse json**  :  
{
  "message": "Livre retourné avec succès."
}


**Codes possibles** : 200 ok , 404 not found, 409 conflicts   

# Consulter les emprunts d'un adhérent  
GET /adherents/{id}/emprunts  

**Body attendu** : aucun  

**reponse json**  :  
[
  {
    "idEmprunt": 42,
    "titre": "papa",
    "dateEmprunt": "2026-07-20",
    "dateRetourPrevue": "2026-08-03"
  },
  {
    "idEmprunt": 43,
    "titre": "Le Petit Prince",
    "dateEmprunt": "2026-07-18",
    "dateRetourPrevue": "2026-08-01"
  }
]


**Codes possibles** : 200 ok , 404 not found

#   


'''  
                           +------------------+
                           |     Auteur       |
                           +------------------+
                           | idAuteur (PK)    |
                           | nom              |
                           | prenom           |
                           +------------------+
                                   |
                             1     |     N
                                   |
                                   |
                           +------------------+
                           |      Livre       |
                           +------------------+
                           | idLivre (PK)     |
                           | titre            |
                           | annee            |
                           | disponible       |
                           | auteur_id (FK)   |
                           | categorie_id(FK) |
                           +------------------+
                                   |
                             N     |     1
                                   |
                           +------------------+
                           |    Catégorie     |
                           +------------------+
                           | idCategorie (PK) |
                           | nom              |
                           +------------------+

                                   |
                             1     |     N
                                   |
                           +------------------+
                           |    Emprunt       |
                           +------------------+
                           | idEmprunt (PK)   |
                           | dateEmprunt     |
                           | dateRetourPrev  |
                           | dateRetour      |
                           | livre_id (FK)   |
                           | adherent_id(FK) |
                           +------------------+
                                   |
                             N     |     1
                                   |
                           +------------------+
                           |    Adhérent      |
                           +------------------+
                           | idAdherent (PK)  |
                           | nom             |
                           | prenom          |
                           | email           |
                           | telephone       |
                           +------------------+


'''
