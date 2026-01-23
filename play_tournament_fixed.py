import os
import sys
import random
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(parent_dir)
from backend.jeu import Jeu
from ia.general import make_general
from tournament_calcul import Tournament


def end_fight(generaux: list, list_unite: dict, swap_positions=False):
    partie = initialiser(generaux, list_unite, swap_positions)
    return partie


def initialiser(generaux: list, list_unite: dict, swap_positions=False):
    if len(generaux) == 1:
        partie = Jeu(generaux[0], generaux[0])
    else:
        partie = Jeu(generaux[0], generaux[1])
    
    liste = []
    for k, v in list_unite.items():
        for i in range(v):
            liste.append(k)
    random.shuffle(liste)
    
    h = partie.carte.hauteur
    mid = h // 2
    x = 0
    taille = len(liste)
    cpt = 0
    
    while taille > h:
        taille //= 2
        x += 1
    
    equipe_gauche = 1 if swap_positions else 0
    equipe_droite = 0 if swap_positions else 1
    
    for i in range(x + 1):
        for j in range(mid - taille // 2, mid - taille // 2 + taille):
            partie.ajouter_unite(f"{liste[cpt]}", i, j, equipe_gauche)
            partie.ajouter_unite(f"{liste[cpt]}", partie.carte.largeur - i - 1, j, equipe_droite)
            cpt += 1
    
    return partie


def tournoi(generaux: list, list_unite: dict, nb_combat=100):
    tournament = Tournament(generaux, {"sc1": list_unite})
    
    for idx_g1 in range(len(generaux)):
        for idx_g2 in range(idx_g1, len(generaux)):
            g1_name = generaux[idx_g1]
            g2_name = generaux[idx_g2]
            
            print(f"\n{'='*50}")
            print(f"  {g1_name} vs {g2_name}")
            print(f"{'='*50}")
            
            for combat_num in range(nb_combat):
                swap = (combat_num % 2 == 1)
                partie = initialiser([g1_name, g2_name], list_unite, swap_positions=swap)
                
                print(f"Combat {combat_num + 1}/{nb_combat} - {len(partie.unites)} unites")
                
                max_tours = 1000
                while partie.check_victory() is None and partie._tour < max_tours:
                    partie.mettre_a_jour()
                
                result = partie.check_victory()
                
                if result == 1:
                    vainqueur = partie.generaux[1].name
                elif result == 2:
                    vainqueur = partie.generaux[0].name
                else:
                    vainqueur = "egalite"
                
                print(f"  -> Vainqueur: {vainqueur} (tour {partie._tour}, {len(partie.unites)} restants)")
                
                tournament.enregistrer_resultat(
                    "sc1",
                    partie.generaux[0].name.lower(),
                    partie.generaux[1].name.lower(),
                    vainqueur.lower()
                )
    
    tournament.generer_rapport_html()


if __name__ == "__main__":
    tournoi(["braindead", "daft"], {"Pikeman": 20, "Knight": 20, "Crossbowman": 20}, 10)
