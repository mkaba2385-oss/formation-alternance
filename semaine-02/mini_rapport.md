# 1. Diagnostic 
ma_fonction1(n) — O(n) : Inefficace. Elle test la divisibilité par un balayage complet de 0 à n-1 réalise n multiplications et n comparaisons. Et  aussi y a pas  l'instruction break dans la fonction ce qui fait elle continue la poursuite de la boucle même après avoir trouvé le résultat.    

ma_fonction2(n) — O(1) : Optimal. L'opérateur modulo % donne le reste de la division entière en temps constant.  

Optimisation : Réécriture de ma_fonction1 avec le calcul direct n % 7 == 0, change la complexité de O(n) à O(1).  
# 2. Coordonnées pour expérimenté   
Paramètre : n = 10 000  
Répétitions : 1 000 exécutions via timeit.timeit  
Formatage : .6f (6 décimales en secondes)  
# 3. Résultats des mesures 
--- RÉSULTATS DES MESURES (n = 10000, 1000 exécutions) ---  
ma_fonction1 (O(n))          : 0.258277 secondes  
ma_fonction2 (O(1))          : 0.000059 secondes  
ma_fonction1_optimisee (O(1)): 0.000055 secondes  
 
L'optimisation a rendu la fonction environ 4 696 fois plus rapide que le premier.
