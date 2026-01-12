from carte import Carte
from Units import Unit  
from jeu import Jeu
from general import *
from vue_terminal import afficher


def scenario_piquiers_vs_chevaliers():  

    # 1. Créer le jeu et la carte
    jeu = Jeu('simple',200,200)
    carte = Carte(200, 200)
    jeu.carte = carte  # si la classe Jeu possède un attribut "carte"

    # 2. Créer les généraux
    general_joueur1 = MajorDAFT(0)
    general_joueur2 = MajorDAFT(1)



    # 3. Ajouter les unités sur la carte
    # --- Piquiers (joueur 1)
    for x in range(3):
        for y in range(5):
            #piquier = Unit("Pikeman")
            #piquier.coords=(x,y)
            jeu.ajouter_unite("Crossbowman",x,y,0) # selon ta classe Jeu
            #carte.placer_unite(piquier, x, y)
              

    # --- Chevaliers (joueur 2)
    for x in range(5, 8):
        for y in range(5):
            #chevalier = Unit("Knight")
            #chevalier.coords=(x,y)
            jeu.ajouter_unite("Crossbowman",x,y,1)
            #carte.placer_unite(chevalier, x, y)
            

    # 4. Ajouter les joueurs au jeu
    #jeu.ajouter_joueur(general_joueur1)
    #jeu.ajouter_joueur(general_joueur2)

    # (optionnel) Afficher la carte
#    afficher(jeu)
    gv = TestGameView(tick=0, units=jeu.unites)
#    jeu.death0[0]=len([u for u in gv.units if u.alive and u.equipe==0])
#    jeu.death1[0]=len([u for u in gv.units if u.alive and u.equipe==1])
    #MajorDAFT pour l'equipe 1 avec un point de regroupement proche
    g1 = MajorDAFT(id_player=0, regroup_at=(4,4))

    #CaptainBraindead pour l'equipe 2 pour voir la difference
    g2 = CaptainBraindead(id_player=1)

    generals = {0:g1, 1:g2}

    TICKS = 20000000

    for _ in range(TICKS):
        print_state(gv)
        tick_simulation(gv, generals)
#        jeu.death0.append(len([u for u in gv.units if u.alive and u.equipe==0]))
#        jeu.death1.append(len([u for u in gv.units if u.alive and u.equipe==1]))
        if check_victory(gv)!=None:
            break
    """
    # 5. Lance et retourner le jeu complet
    while jeu.est_termine()!=True:
        jeu.mettre_a_jour()
    jeu.graphic()"""
#    jeu.graphic(_)
    return jeu

if __name__ == "__main__":
    jeu = scenario_piquiers_vs_chevaliers()
    #jeu.lancer()  # ou toute autre méthode pour démarrer le jeu



