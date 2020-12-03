#!/usr/bin/env python3
"""
Ce module permet de calculer et d'afficher un gif permettant de calculer
une approximation de pi à partir de la méthode de Monte Carlo
"""
import sys
import subprocess
from collections import namedtuple
import simulator as s

Point = namedtuple('Point','x y')

if len(sys.argv)<4:
    raise AttributeError
Taille = int(sys.argv[2])
n = int(sys.argv[1])
VIRGULE = int(sys.argv[3])
if VIRGULE > 25:
    print("Il y a trop de zero à afficher, la limite est 25")
    VIRGULE = 25

def transfo_dimension(point):
    """
    Permet de transformer des points de [-1,1] en des points
    de [0,Taille]
    """
    newpoint = []
    for coord in point:
        newx = int((coord[0].x + 1)*(Taille//2))
        newy = int((coord[0].y + 1)*(Taille//2))
        newpoint.append([Point(newx,newy),coord[1]])
    return newpoint

rawcontent = [['1 1 1  ' for i in range(Taille)] for k in range(Taille)]
# Contenu de l'image sans l'affichage de pi
listepoint,listepi = s.simu(1000000)

ListePointC = transfo_dimension(listepoint)


def generate_ppm_file(numero_image,listpi,listepnt,rawcont):
    """
    Fonction principale générant une image ppm
    """
    pi_string = str(listpi[numero_image])
    if len(pi_string) <= 2 + VIRGULE:
        pi_string += '0'*(2 + VIRGULE - len(pi_string) +1)
    decimal_de_pi = pi_string[2:2 + VIRGULE]

    image = open(f'img{numero_image}_3-{decimal_de_pi}.ppm','x')
    image.write("P3 \n")
    image.write(f"{Taille} {Taille} \n")
    image.write("1 \n")

    for point in listepnt[(n//10)*numero_image:(n//10)*(numero_image+1)]:
        if point[1]:
            rawcont[point[0].y][point[0].x] = '1 0 0 '

        else:
            rawcont[point[0].y][point[0].x] = '0 0 1 '

    decimal_de_pi = '.' + decimal_de_pi
    content = affichage_nombre(decimal_de_pi,rawcontent)
    strcontent = ""
    for coordy in range(Taille):
        for coordx in range(Taille):
            strcontent += content[coordy][coordx]
        strcontent += '\n'
    image.write(strcontent)
    subprocess.call(f"convert  img{numero_image}_3-{decimal_de_pi[1:]}.ppm "
    +f"img{numero_image}_3-{decimal_de_pi[1:]}.ppm", shell=True)
    return rawcontent

def affichage_nombre(decimal_de_pi,rawcont):
    """
    Affiche l'approximation de pi sur l'image
    """
    content = []
    for pts in rawcont:
        content.append(list(pts))

    nombre_pi = affichage_chiffre(3,True)
    for chiffre in decimal_de_pi[:-1]:
        ch_temp = affichage_chiffre(chiffre,True)
        nombre_pi = fusion(nombre_pi,ch_temp)
    nombre_pi = fusion(nombre_pi,affichage_chiffre(decimal_de_pi[-1],False))

    for coordx in range(Taille//2 - len(nombre_pi[0])//2, Taille//2 + len(nombre_pi[0])//2):
        for coordy in range(Taille//2 - len(nombre_pi)//2, Taille//2 + len(nombre_pi)//2):
            if nombre_pi[coordy - Taille//2 + len(nombre_pi)//2][coordx - Taille//2
            + len(nombre_pi[0])//2] == '0 0 0  ':
                content[coordy][coordx] = nombre_pi[coordy - Taille//2
                + len(nombre_pi)//2][coordx - Taille//2 + len(nombre_pi[0])//2]
    return content

def fusion(liste1,liste2):
    """
    Fusionne deux listes en une seule en additionnant les lignes
    une à une
    """
    for element in range(len(liste1)):
        liste1[element] += liste2[element]
    return liste1

def affichage_chiffre(chiffre,space):
    """
    Affiche chaque chiffre de manière individuelle
    """

    ratio = 20 ## Multiple de 10 = plus beau
    hauteur = Taille//10
    largeur = hauteur//3
    pixel = hauteur//ratio
    espace = [['1 1 1  ' for i in range(pixel)] for j in range(hauteur)]

    if chiffre == '.':
        virgule = [['1 1 1  ' for i in range(pixel*2)] for j in range(hauteur)]
        for i in range(pixel//2,3*pixel//2):
            for j in range(hauteur - pixel,hauteur):
                virgule[j][i] = '0 0 0  '
        if space :
            return fusion(virgule,espace)
        return virgule

    chiffretab = [['1 1 1  ' for _ in range(largeur)] for i in range(hauteur)]
    chiffre = int(chiffre)

    if chiffre not in (1,4):
        ## Afficher barre en haut
        for i in range(pixel):
            for j in range(largeur):
                chiffretab[i][j] = '0 0 0  '
    if chiffre not in (5,6):
        ## barre en haut à droite
        for i in range(hauteur//2):
            for j in range(largeur - pixel,largeur):
                chiffretab[i][j] = '0 0 0  '
    if chiffre != 2:
        ## barre en bas à droite
        for i in range(hauteur//2,hauteur):
            for j in range(largeur - pixel,largeur):
                chiffretab[i][j] = '0 0 0  '
    if chiffre not in (4,1,7):
        ## barre du bas
        for i in range(hauteur-pixel, hauteur):
            for j in range(largeur):
                chiffretab[i][j] = '0 0 0  '

    if chiffre in (2,8,6,0):
        ## barre en bas à gauche
        for i in range(hauteur//2,hauteur):
            for j in range(pixel):
                chiffretab[i][j] = '0 0 0  '
    if chiffre not in (1,2,3):
        ## barre en haut à gauche
        for i in range(hauteur//2):
            for j in range(pixel):
                chiffretab[i][j] = '0 0 0  '
    if chiffre not in (1,7,0):
        ## Barre milieu
        for i in range(hauteur//2 - pixel//2,hauteur//2 + pixel//2):
            for j in range(largeur):
                chiffretab[i][j] = '0 0 0  '
    if space :
        return fusion(chiffretab,espace)
    return chiffretab

for num in range(10):
    generate_ppm_file(num,listepi,ListePointC,rawcontent)

NOM = "*.ppm"
OUTPUT = "output.gif"
subprocess.call("convert -delay 100 " + NOM + " " + OUTPUT, shell=True)
