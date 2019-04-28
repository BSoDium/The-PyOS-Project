'''
On se propose de déterminer quand un astre se trouve dans le champ de vision, ce qui implique dans un premier temps 
de connaître l'angle de vision. Celui-ci est très probablement réglable, mais en l'absence de données supplémentaires, 
il sera préférable de procéder à un calibrage:  On crée une 'règle graduée', et on place la caméra à un position connue, 
face à cette règle étalon. On lit alors les valeurs sur la règle au niveau des bords de l'écran, ce qui nous permetttra d'en déduire
l'angle alpha max

--> probleme: la résolution de l'écran est variable
--> solution: automatiser ce calcul, mais comment ?

