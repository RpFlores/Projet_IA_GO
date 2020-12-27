Mathis Fuentes
Roxane Flores

points forts:
-assez rapide (suivant l'horizon)
-joue très correctement
-il arrive à bien évaluer les plateaux

On a deux heuristiques :

-Une première qui calcule le nombre de pièces qu'on a sur le plateau. On avait fait une première version qui appelait computeScore()
mais il s'avère que compter les caillous est tout autant efficace et plus rapide. 

-La deuxième qui privilégie de poser une pièce à côté d'autres pièces de la même couleur pour former une chaine.
Mais pour autant elle veut éviter de fermer des issus, ne pas placer une pièces alors que ses 4 voisins sont de la même couleur.
De même, on évite de trop se placer sur les bords pour ainsi tenter de capturer le plus de zones possibles.


Nous sommes tout particulièrement fier d'avoir pu implémenter Monte carlo Tree Search qui malgré tout ne peut pas être utilisé car 
il demande trop de temps de calcul pour pouvoir faire un nombre de rollout pertinent (on bloque à une centaine alors qu'il faudrait
en faire plus d'un millier au minimum). De plus Monte Carlo fonctionne exactement comme souhaité, sans bugs.
/!\ Pour pouvoir faire tourner monte carlo (avec 100 itérations) il faut décommenter la partie indiquée
	dans getPlayerMove() de myPlayer.py (et commenter la partie Alpha Beta)

De plus, nous avons implémenté un set de coups de bases, qui sont des bons coups à jouer en début de partie. Donc tant que notre joueur 
voit qu'un de ces coups est disponible, il va le jouer. Ces coups favorisent la prise des angles du plateau.

myPlayer tourne par défaut avec alpha beta qui va en profondeur 3 car notre joueur prend aux alentours des 4 minutes de jeu qui est en dessous 
de la limite. Le score est calculé en faisant la somme des 2 heuristiques.

Monte carlo nous a pris un peu de temps à implémenter et nous avons appris tardivement que ce n'était pas le choix optimal, nous avons donc eu
moins de temps pour approfondir notre heuristique et tenter de l'améliorer.

