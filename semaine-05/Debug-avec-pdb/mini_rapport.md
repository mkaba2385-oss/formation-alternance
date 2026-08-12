# commande pdb utilisée
- l : afficher le code autour. elle a servi de voir les codes écrit en haut et en bas du breakpoint(). 
- s : entrer dans la fonction. Elle a servi d’entrer dans la fonction ou il a le bug.
- w : where (call stack). Elle a servi a vérifier qu’on est bien a l’intérieur de la fonction.
- n : ligne suivante. Elle a servi défiler chaque ligne de la fonction pour identifier le bug.
- p result : afficher. Elle a servi a voir que la variable result n’est pas définit.
- c : jusqu au prochain breakpoint. Elle a servi a voir AssertionError.


# Retours d'expérience 

- Reproduction : En appelant la fonction décorée la valeur de retour obtenue était None au lieu du résultat attendu (6.7).  

- Isolation avec pdb : En faisant un s au moment de l'appel de la fonction pdb m'a dirigé dans le wrapper du décorateur dans utils.py.  

- Compréhension : Grâce à p result  j'ai vérifié que la fonction décorée fonctionnait correctement (result = 6.7). Cependant en faisant n la fonction wrapper s'est terminée sans retourner cette valeur.  

- Correction : j'ai ajouter return result à la fin de wrapper.
