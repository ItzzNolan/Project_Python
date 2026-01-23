import os
import sys
import random
parent_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(parent_dir)
from backend.jeu import Jeu
from ia.general import make_general
from tournament_calcul import Tournament

def end_fight(generaux:list, list_unite:list):
    # faire tout les trucs d'affichage
    partie= initialiser(generaux, list_unite)

    return partie

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
            partie.ajouter_unite(f"{liste[cpt]}",partie.carte.largeur-i-1,j,1)
            cpt+=1
    # dict={}
    # for unite in list_unite:
    #     if list_unite[unite]>h:
    #         if list_unite[unite]%2==1:
    #             dict[f"{unite}2"]=list_unite[unite]//2 +1
    #             list_unite[unite]//=2
    #         else:
    #             dict[f"{unite}2"]=list_unite[unite]//2
    #             list_unite[unite]//=2
    # list_unite.update(dict)
    # for unite in list_unite:
    #     for y in range(mid-list_unite[unite]//2,mid-(list_unite[unite]//2) + list_unite[unite]):
    #         if y%2==0:
    #             partie.ajouter_unite(f"{unite}",x,y,0)
    #         partie.ajouter_unite(f"{unite}",partie.carte.largeur-x-1,y,1)
    #         cpt+=1
    #     # print(partie.carte.largeur-x)
    #     x+=1
    # print([[u.Unit,u.coords] for u in partie.unites])
    # print(cpt)
    # print([u.Unit for u in partie.unites],[u.equipe for u in partie.unites] )
    return partie


def tournoi(generaux:list, list_unite:dict,nb_combat=100):
    # tournament=Tournament(generaux,[list_unite])
    unites=list_unite
    partie=initialiser(generaux, list_unite)
    vainqueur=""
    for g1 in generaux:
        partie.generaux[0]=make_general(f"{g1}",0)
        for g2 in generaux:
            partie.generaux[1]=make_general(f"{g2}",1)
            print(f"combat :{partie.generaux[0]} vs {partie.generaux[1]}")
            print(f"nb unite : {len(partie.unites)}")
            for i in range(nb_combat):
                vainqueur=""
                print(f"combat n°{i+1}")
                while partie.check_victory()==None:
                    partie.mettre_a_jour()
                    # print([[u.Unit,u.coords, u.HP] for u in partie.unites])
                    # print(f"tour: {partie._tour} , unite:{len(partie.unites)}")
                if partie.check_victory()==1:
                    vainqueur=partie.generaux[0].name
                    print(f"vainqueur: {partie.generaux[0].name}1 avec {len(partie.unites)} unites")
                elif partie.check_victory()==2:
                    vainqueur=partie.generaux[1].name
                    print(f"vainqueur: {partie.generaux[1].name}2 avec {len(partie.unites)} unites")
                print([u.equipe for u in partie.unites])
                # tournament.enregistrer_resultat(partie.generaux[0].name,partie.generaux[1].name,vainqueur)
                partie = end_fight([g.name for g in partie.generaux.values()], list_unite)
    # tournament.generer_rapport_html()


if __name__ == "__main__":
    tournoi(["braindead"],{"Pikeman":20, "Knight":20, "Crossbowman":20})