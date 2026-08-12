# POST-MORTEM : Problème de données à cause d’un état partagé dans le cache

## 1. Symptômes  
Quand je demandait la météo de la région NORD, il pouvait recevoir une température de 42.0°C alors que la bonne valeur était 38.5°C. La valeur 42.0°C correspondait normalement à la région SUD.

## 2. Hypothèses écartées   
Problème avec le provider météo (MockWeatherProvider) : Après vérification des logs le provider retournait bien la bonne valeur de 38.5°C. Donc le problème ne venait pas de lui.

## 3. cause profonde
le problème venait du cache dans CachedWeatherProvider on modifiait directement une donnée partagée au lieu de travailler sur une copie.

## 4. correction  
Pour régler le problème j’ai fait une copie de l’objet avant de le modifier avec :

**res = self._cache[region].model_copy(deep=True)**

Comme ça je travaille sur une nouvelle copie de MeteoData et je ne modifie plus directement l’objet qui est dans le cache.

## 5. comment éviter à l'avenir  
Éviter de modifier directement les objets qui sont dans le cache Il faut travailler sur une copie.
