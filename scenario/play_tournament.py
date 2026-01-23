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
    #fatiha -> ptit chnangetln
    swap = (combat_num % 2 == 1)  # Alterne à chaque combat
    partie = initialiser([g1_name, g2_name], list_unite, swap_positions=swap)

    return partie

def initialiser(generaux:list, list_unite:dict):
    if len(generaux)==1:
        partie = Jeu(generaux[0], generaux[0])
    else:
        partie = Jeu(generaux[0], generaux[1])
    
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
    tournament=Tournament(generaux,{"sc1":list_unite})
    unites=list_unite
    partie=initialiser(generaux, list_unite)
    vainqueur=""
    for idx_g1 in range(len(generaux)):
        partie.generaux[0]=make_general(f"{generaux[i]}",0)
        for j in range(i,len(generaux)):
            partie.generaux[1]=make_general(f"{generaux[j]}",1)
            print(f"combat :{partie.generaux[0]} vs {partie.generaux[1]}")
            print(f"nb unite : {len(partie.unites)}")
            #fatiha-> je ense là i est ecrase
            for idx_g2 in range(nb_combat):
                vainqueur=""
                print(f"combat n°{i+1}")
                #je pense qu'il faut pas avoir de jeu infinie
                max_tours = 1000
                while partie.check_victory() is None and partie._tour < max_tours:
                    partie.mettre_a_jour()
                    # print([[u.Unit,u.coords, u.HP] for u in partie.unites])
                    # print(f"tour: {partie._tour} , unite:{len(partie.unites)}")
                if partie.check_victory()==1:
                    vainqueur=partie.generaux[0].name
                    print(f"vainqueur: {partie.generaux[0].name} avec {len(partie.unites)} unites")
                elif partie.check_victory()==2:
                    vainqueur=partie.generaux[1].name
                    print(f"vainqueur: {partie.generaux[1].name} avec {len(partie.unites)} unites")
                else:
                    vainqueur="egalite"
                    print(f"vainqueur: aucun, egalite")
                tournament.enregistrer_resultat("sc1",partie.generaux[0].name.lower(),partie.generaux[1].name.lower(),vainqueur)
                partie = end_fight([g.name for g in partie.generaux.values()], list_unite)
    tournament.generer_rapport_html()


if __name__ == "__main__":

    tournoi(["captain braindead","major daft"],{"Pikeman":20, "Knight":20, "Crossbowman":20}, 10)
