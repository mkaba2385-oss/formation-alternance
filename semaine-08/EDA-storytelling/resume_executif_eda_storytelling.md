# Résumé exécutif — EDA + storytelling business

## Contexte

L'analyse porte sur le dataset `tips`, un jeu de données de transactions de restaurant comprenant **244 transactions**. Après suppression d'un doublon exact, **243 transactions** sont utilisées pour les agrégations métier.

L'objectif est de passer d'une simple description des données à des **recommandations actionnables**.

## Les principaux insights

### 1. Sécuriser le samedi
Le samedi concentre le plus gros volume (**87 transactions**) et le plus gros chiffre d'affaires observé (**1 778,40**).

**Recommandation :** renforcer la capacité opérationnelle le samedi : staffing, disponibilité des tables et gestion des temps d'attente. Suivre les transactions perdues et le temps d'attente.

### 2. Tester l'upsell le dimanche
Le dimanche présente le **ticket moyen le plus élevé : 21,41**.

**Recommandation :** tester une proposition d'upsell (dessert, boisson ou accompagnement) le dimanche et mesurer l'effet sur le ticket moyen.

### 3. Cibler les groupes de 3–4 personnes
Le ticket moyen passe d'environ **16,45 pour 2 personnes** à **23,28 pour 3** et **28,61 pour 4**.

**Recommandation :** créer une formule de partage ou un menu groupe pour 3–4 personnes. Vérifier l'impact sur le temps de service et la capacité.

### 4. Utiliser le déjeuner comme terrain de test
Le déjeuner génère environ **1 167,47** de chiffre d'affaires dans l'échantillon, avec un ticket moyen de **17,17**, contre **20,80** au dîner.

**Recommandation :** tester une formule déjeuner avec un complément à forte valeur perçue afin d'augmenter le ticket moyen.

## Qualité et limites

Aucune valeur manquante n'est présente. Un doublon exact a été identifié puis exclu des agrégations. Quelques valeurs atypiques existent, notamment sur le pourcentage de pourboire ; elles doivent être surveillées mais pas supprimées sans justification.

Le dataset est petit et destiné à la démonstration. Les résultats ne doivent donc pas être généralisés à un restaurant réel sans validation sur plusieurs semaines de données.

## Plan d'action

1. **Samedi :** protéger le chiffre d'affaires existant.
2. **Dimanche :** expérimenter l'upsell.
3. **Groupes 3–4 :** tester une offre dédiée.
4. **Déjeuner :** expérimenter une formule d'augmentation du panier.

Les KPI de suivi recommandés sont : chiffre d'affaires, ticket moyen, nombre de transactions, temps d'attente et taux d'adoption des offres.
