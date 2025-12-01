from backend.carte import Carte
from backend.Units import Unit  
from backend.jeu import Jeu
from ia.general import MajorDAFT


def scenario_piquiers_vs_chevaliers():  

    # 1. Créer le jeu et la carte
    jeu = Jeu()
    carte = Carte(10, 10)
    jeu.carte = carte  # si la classe Jeu possède un attribut "carte"

    # 2. Créer les généraux
    general_joueur1 = MajorDAFT("Joueur 1")
    general_joueur2 = MajorDAFT("Joueur 2")

    # 3. Ajouter les unités sur la carte
    # --- Piquiers (joueur 1)
    for x in range(3):
        for y in range(10):
            piquier = Unit("Piquier")
            carte.placer_unite(piquier, x, y)
            jeu.ajouter_unite(general_joueur1, piquier)  # selon ta classe Jeu

    # --- Chevaliers (joueur 2)
    for x in range(7, 10):
        for y in range(10):
            chevalier = Unit("Chevalier")
            carte.placer_unite(chevalier, x, y)
            jeu.ajouter_unite(general_joueur2, chevalier)

    # 4. Ajouter les joueurs au jeu
    jeu.ajouter_joueur(general_joueur1)
    jeu.ajouter_joueur(general_joueur2)

    # (optionnel) Afficher la carte
    carte.afficher()

    # 5. Retourner le jeu complet
    return jeu

if __name__ == "__main__":
    jeu = scenario_piquiers_vs_chevaliers()
    jeu.lancer()  # ou toute autre méthode pour démarrer le jeu




