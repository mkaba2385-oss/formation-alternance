# historique des dernières pages visitées 
**structure** : pile (stack)  / collections.deque
**justification** : l’historique de navigation fonctionne selon le principe LIFO(dernier entré, premier sorti) la dernière page visitée est toujours la première a être retirée quand on clique sur le bouton retour. L'utilisation d'une deque (avec le paramètre maxlen) est idéale ici car elle permet d'exécuter les opérations d'ajout et de retrait rapidement en temps constant O(1) tout en supprimant automatiquement les plus anciennes pages visitées dès que la limite d'historique est atteinte.
# catalogue de livres avec accès rapide par ISBN  
**structure** :  Dictionnaires (dict)     
**justification** : le dictionnaire est parfait ici car chaque livre possède un numéro ISBN unique qui sert la clé. Cela permet de retrouver directement toutes les infos d’un livre (titre, auteur, etc..) grâce a son ISBN sans avoir a parcourir toute la liste, ce qui rend la recherche rapide en 0(1).
# suivi des joueurs actifs (ajout/retrait fréquents)
**structure** :  Ensemble (set)   
**justification** : comme les joueurs se connectent et déconnectent tout le temps, le set permet d’ajouter ou de supprimer un joueur très rapidement en 0(1). Il empêche automatiquement les doublons ce qui évite d’avoir un même joueur compté deux fois par erreur.
# configuration d'app (clés stables, valeurs varient)
**structure** :  Dictionnaire (dict)   
**justification** : un dictionnaire fonctionne avec un système de clé et de valeurs (par exemple "Sini" : "application"). Les noms des paramètres (les clés) restent toujours les mêmes mais on peut facilement modifier la valeur associée a n’importe quel moment dans le code sans devoir reconstruire toute la structure. 
# undo/redo dans un éditeur
**structure** :  Deux piles (stacks/ list ou deque )   
**justification** : utiliser deux piles une pour undo et une pour redo. Respecte le principe LIFO (dernier arrivé, premier sorti) indispensable pour annuler ou rétablir des actions. Annuler dépile une action de la pile undo pour l’empiler sur la pile redo, le tout en 0(1). 


# classement de scores triés 
**structure** :  liste de tuples (list)  
**justification** : on utilise une liste contenant des tuples du types (joueur, score). Le tuple permet d’associer le nom du joueur a son score, et la liste permet de garder un classement ordonné. Contrairement a d’autres structures la liste accepte les doublons si deux joueurs ont exactement le même score, et on peut simplement la trier avec la fonction sort().

# notifications à traiter dans l'ordre
**structure** :  collections.deque  
**justification** : pour traiter des notifications dans l’ordre d’arrivée il faut respecter la logique FIFO (premier arrivé, premier sorti). On utilise deque car elle permet d’ajouter très rapidement des éléments a la fin avec .append() et de retirer la plus ancienne notifications  au début avec .popleft() le tout en temps constant. 

# tags uniques d'un article 
**structure** :  Ensemble (set)  
**justification** : un set élimine automatiquement les doublons si un même tag est ajouté plusieurs fois à un article. Il permet également d’effectuer très facilement des opérations de filtrage ou de croisement de tags entre plusieurs articles (intersections, unions)


