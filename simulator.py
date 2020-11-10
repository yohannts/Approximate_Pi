#!/usr/bin/env python3

"""
Module ne contenant que la simulation de pi
"""

## Importation des modules
import sys
import random as rdm
from collections import namedtuple

## Déclaration des variables globales
Point = namedtuple('Point','x y') ## Definition d'un point à partir d'un namedtuple
BON_ARG = True ## Variable visant le bon fonctionnement de la demande de
#l'utilisateur dans la console

if len(sys.argv) == 1: ## S'il n'y a pas d'argument, le programme ne tourne pas
    print("La commande d'execution est < ./simulator.py nombre_de_points > ")
    BON_ARG = False
else : ## Eventuellement ajouter le cas où ce n'est pas un nombre entier
    np = int(sys.argv[1])

## Script
def simu(nbr):
    """
    Fonction qui permet de calculer des points aléatoires sur un carré
    de [-1,1] pour calculer pi
    """
    compteur_dans_cercle = 0 ## Compteur de point dans le cercle
    listepoint,listepi = [],[]
    for i in range(10):
        for _ in range(nbr//10):
            pnt = Point(rdm.randrange(-nbr,nbr)/nbr,rdm.randrange(-nbr,nbr)/nbr)
            ## On génère des entiers, puis on les transforme en réel entre -1 et 1
            if (pnt.x**2 + pnt.y**2) <= 1: ## Si le point est dans le cercle
                compteur_dans_cercle += 1
                listepoint.append([pnt,True])
            else :
                listepoint.append([pnt,False])
        pic = 10*4*compteur_dans_cercle/(nbr*(i+1)) ## Revoit l'estimation de pi
        listepi.append(pic)
    print(listepi[-1])
    return listepoint, listepi

if __name__ == '__main__':
    if BON_ARG:
        simu(np)
