# si un commit important est disparu et tu ne sais pas comment récupérer suis ses étapes:
Tape la commande : git reflog  
Sa t’affiche l'historique des commit  
Identifie le numéro de la commit à récupérer  
Créer une nouvelle branche et bascule sur la branche avec la commande : git switch -c nom_de_la_branche  
Tape la commande : git cherry-pick suivie_du_numero_de_la_commit_a_récupérer  

