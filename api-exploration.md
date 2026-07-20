# liste tous les users
curl -i -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n" https://jsonplaceholder.typicode.com/users  

**taille** : 5645 octets  
**code** : 200


# récupère le user 3  
curl -i -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n" https://jsonplaceholder.typicode.com/users/3  

**taille** : 520 octets   
**code** : 200  

# ses posts  
curl -i -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n" https://jsonplaceholder.typicode.com/users/3/posts  

**taille** : 2661 octets   
**code** : 200 

# les commentaires du post 1
curl -i -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n" https://jsonplaceholder.typicode.com/posts/1/comments  

**taille** : 1510 octets   
**code** : 200   

# Fais un POST pour créer un post fictif  
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
   -H "Content-type: application/json; charset=UTF-8" \
   -d '{"title" : "Mon nouveau post", "body": "contenu du post ", "userId" : 1}' \
   -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n"  

**taille** : 91 octets   
**code** : 201  

# un PUT pour modifier    
curl -i -X PUT https://jsonplaceholder.typicode.com/posts/1 \
   -H "Content-type: application/json; charset=UTF-8" \
   -d '{"title" : "Mon nouveau post2", "body": "contenu du post2 ", "userId" : 1}' \
   -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n"  


**taille** : 91 octets   
**code** : 200  

# un DELETE pour supprimer  
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1 \
  -w "\n\n--- INFOS ---\nCode HTTP : %{http_code}\nTaille : %{size_download} octets\n"  


**taille** : 2 octets   
**code** : 200

