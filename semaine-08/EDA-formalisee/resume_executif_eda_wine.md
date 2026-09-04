# Résumé exécutif — EDA du dataset Wine

## Objectif

Cette EDA avait pour objectif d'explorer le dataset **Wine** de `scikit-learn` en partant de 10 questions définies avant l'analyse. Le dataset contient **178 vins**, 13 variables chimiques et 3 classes de vins.

## Principaux constats

- **Qualité des données :** aucune valeur manquante et aucun doublon. Le dataset est donc propre pour l'analyse.
- **Répartition des classes :** 59 vins en classe 0, 71 en classe 1 et 48 en classe 2. Les classes sont légèrement déséquilibrées, mais restent suffisamment représentées.
- **Alcool :** la médiane est de 13,05 et 50 % des observations se trouvent entre 12,36 et 13,68.
- **Dispersion :** la proline possède de loin la plus forte dispersion, avec un écart-type d'environ 315.
- **Relations entre variables :** le taux d'alcool et la proline ont une corrélation positive de 0,64. Plusieurs autres variables présentent également des corrélations fortes, ce qui montre qu'une partie de l'information est redondante.
- **Différences entre classes :** le taux d'alcool moyen est de 13,74 pour la classe 0, 12,28 pour la classe 1 et 13,15 pour la classe 2.
- **Flavanoïdes :** cette variable différencie particulièrement bien les classes : moyenne de 2,98 en classe 0, 2,08 en classe 1 et 0,78 en classe 2.
- **Valeurs atypiques :** quelques observations peuvent être considérées comme atypiques selon la règle de l'IQR, notamment pour la proline. Elles ne doivent pas être supprimées sans justification.
- **ACP :** les deux premières composantes expliquent environ **55,4 %** de la variance totale et permettent de visualiser une séparation assez nette des trois classes.

## Conclusion

L'EDA montre que les caractéristiques chimiques du vin contiennent une information importante pour distinguer les trois classes. Les variables comme les **flavanoïdes**, la **proline** et l'**alcool** ressortent comme particulièrement intéressantes.

Le dataset est suffisamment propre pour passer à une étape de modélisation. La prochaine étape logique serait de construire un modèle de classification, puis de vérifier quantitativement quelles variables contribuent réellement le plus à la prédiction des classes.
