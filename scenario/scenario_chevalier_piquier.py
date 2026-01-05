from backend.carte import Carte
from backend.Units import Unit  
from backend.jeu import Jeu
from ia.general import MajorDAFT
from frontend.vue_terminal import afficher

def scenario_piquiers_vs_chevaliers():  

    # 1. Créer le jeu et la carte
    jeu = Jeu()
    carte = Carte(10, 10)
    jeu.carte = carte  # si la classe Jeu possède un attribut "carte"

    # 2. Créer les généraux
    general_joueur1 = MajorDAFT(0)
    general_joueur2 = MajorDAFT(1)

    # 3. Ajouter les unités sur la carte
    # --- Piquiers (joueur 1)
    for x in range(3):
        for y in range(10):
            #piquier = Unit("Piquier")
            #carte.placer_unite(piquier, x, y)
            jeu.ajouter_unite("Pikeman",x,y,0)  # selon ta classe Jeu

    # --- Chevaliers (joueur 2)
    for x in range(7, 10):
        for y in range(10):
            #chevalier = Unit("Chevalier")
            #carte.placer_unite(chevalier, x, y)
            jeu.ajouter_unite("Knight",x,y,1)

    # 4. Ajouter les joueurs au jeu
    #jeu.ajouter_joueur(general_joueur1)
    #jeu.ajouter_joueur(general_joueur2)

    # (optionnel) Afficher la carte
    jeu.carte.afficher()

    # 5. Lancer et retourner le jeu complet
    while not jeu.est_termine():
        jeu.mettre_a_jour()
    return jeu





