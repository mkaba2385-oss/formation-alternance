## ce que j’ai fais
Créer le fichier notes.md en ajoutant 5 lignes a l’intérieur.
git add notes.md
git commit -m "docs: ajouter notes.md avec 5 lignes"
créer la branche feat section-a
git checkout -b feat/section-a
Modifier les lignes 1 et 2 manuellement.
git add notes.md
git commit -m "feat: mise a jour de la ligne 1 et 2 par la section-a"
Retourner sur la branche main avec : git checkout main
Créer la branche feat/section-b 
git checkout -b feat/section-b
Modifier les lignes 1 et 2 différemment.
git add notes.md
git commit -m "feat: mise a jour de la ligne 1 et 2 par la section-b"
git merge feat/section-a
git merge feat/section-b (le conflit a été déclencher et un fichier ses ouvert avec des indices dessus j’ai nettoyer le fichier manuellement pour garder les 5 lignes que je voulais garder puis enregistré )
git add notes.md
git commit -m "chore: corriger le conflit de fusion avec feat/section-b"

## ce qui a été difficile
Résoudre manuellement le conflit entre fusion de section a et b après j’ai suis supprimer ce que je voulais pas garder avec les balises qui signalait l’erreur  les lignes puis le sauvegarder  




