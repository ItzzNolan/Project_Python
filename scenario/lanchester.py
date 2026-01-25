import random
import os
import sys
parent_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(parent_dir)
from backend.jeu import Jeu

def initialiser(generaux:list, list_unite:dict):
    if len(generaux)==1:
        partie = Jeu(generaux[0], generaux[0])
    else:
        partie = Jeu(generaux[1], generaux[0])
    
    liste=[]
    for k,v in list_unite.items():
        for i in range(v):
            liste.append(k)
    random.shuffle(liste)
    h=partie.carte.hauteur
    mid=h//2
    x=0
    taille=len(liste)
    cpt=0
    while taille>h:
        taille//=2
        x+=1
    for i in range(x+1):
        for j in range(mid-taille//2,mid-taille//2+taille):
            partie.ajouter_unite(f"{liste[cpt]}",i,j,0)
            partie.ajouter_unite(f"{liste[cpt]}",partie.carte.largeur-2*i-1,j,1)
            partie.ajouter_unite(f"{liste[cpt]}",partie.carte.largeur-2*i-2,j,1)
            cpt+=1
    return partie

def lanchester(type, nombre):
    if type.lower()=='melee':
        jeu=initialiser(["daft"],{"Pikeman":nombre})
    elif type.lower()=='archer':
        jeu=initialiser(["daft"],{"Crossbowman":nombre})
    while jeu.check_victory()==None:
        jeu.mettre_a_jour()
    jeu.graphic(jeu._tour,f"{type}")


if __name__ == "__main__":
    lanchester('melee',100)