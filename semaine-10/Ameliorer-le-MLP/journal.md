## Exercice 48.1 — Améliorer le MLP

### Résultats

| Expérience           | Train accuracy | Test accuracy |   Temps |
| -------------------- | -------------: | ------------: | ------: |
| Baseline             |        97.86 % |       97.92 % | 171.1 s |
| Learning rate = 1e-2 |        89.34 % |       94.21 % | 138.5 s |
| Learning rate = 1e-4 |        97.03 % |       97.58 % | 165.3 s |
| Dropout = 0.5        |        96.21 % |       97.75 % | 121.4 s |
| Sans dropout         |        99.26 % |       97.57 % | 159.1 s |
| Batch size = 256     |        98.18 % |       98.15 % |  73.7 s |

### Observations

Le modèle de référence avec un learning rate de 1e-3, un dropout de 0.3 et une batch size de 64 atteint 97.92 % d'accuracy sur le jeu de test.

Avec un learning rate de 1e-2, les performances diminuent fortement : le test accuracy tombe à 94.21 %. Le learning rate est trop élevé pour cette configuration et les mises à jour des poids sont trop importantes.

Avec un learning rate de 1e-4, le modèle atteint 97.58 % de test accuracy. L'apprentissage est plus lent, mais le modèle finit par atteindre une bonne performance après 10 epochs.

En augmentant le dropout à 0.5, le train accuracy diminue à 96.21 %, tandis que le test accuracy reste proche de la baseline avec 97.75 %. Le dropout augmente donc la régularisation.

Sans dropout, le train accuracy monte à 99.26 %, mais le test accuracy est de 97.57 %. L'écart entre les deux performances augmente, ce qui montre un risque de surapprentissage (overfitting).

Avec une batch size de 256, le temps d'entraînement diminue fortement, passant de 171.1 secondes à 73.7 secondes. Le test accuracy atteint 98.15 %. Dans cette expérience, le batch plus grand permet donc un entraînement beaucoup plus rapide tout en conservant de bonnes performances.

### Conclusion

Cette expérience montre que le choix des hyperparamètres influence fortement l'entraînement d'un réseau de neurones.

Le learning rate doit être suffisamment petit pour permettre une convergence stable sans rendre l'apprentissage inutilement lent. Le dropout permet de limiter le surapprentissage. La batch size influence le nombre de mises à jour et le temps d'entraînement.

La différence entre train accuracy et test accuracy est également importante pour détecter l'overfitting.
