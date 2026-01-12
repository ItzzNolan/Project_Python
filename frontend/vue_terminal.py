# frontend/vue_terminal.py

import colorama
from colorama import Fore, Back, Style

from backend.carte import Carte

debug_mode = True
DEBUG = 1 if debug_mode else 0


def afficher(jeu):
    """
    Affiche l'état complet du jeu en se basant sur l'objet Jeu réel.
    
    Arguments:
        jeu: L'objet principal du jeu, qui contient la carte et la liste des unités.
    """
    colorama.init(autoreset=True)

    carte = jeu.carte
    
    # 1. On prépare la "toile" vide
    grille_affichage = [[f"{Fore.GREEN} . {Style.RESET_ALL}" for _ in range(carte.largeur)] for _ in range(carte.hauteur)]

    # 2. Créer un dictionnaire pour regrouper les unités par case
    unites_par_case = {}
    for unite in jeu.unites:
        if not unite.alive:
            continue
        
        x_float, y_float = unite.coords
        # Arrondir à la case la plus proche
        x_case = round(x_float)
        y_case = round(y_float)
        
        if 0 <= x_case < carte.largeur and 0 <= y_case < carte.hauteur:
            cle = (x_case, y_case)
            if cle not in unites_par_case:
                unites_par_case[cle] = []
            unites_par_case[cle].append(unite)
    
    # 3. Afficher les unités
    for (x, y), unites in unites_par_case.items():
        if len(unites) == 1:
            # Une seule unité
            unite = unites[0]
            initiale = unite.Unit[0].upper()
            couleur = Fore.BLUE if unite.equipe == 0 else Fore.RED
            grille_affichage[y][x] = f"{couleur} {initiale} {Style.RESET_ALL}"
        else:
            # Plusieurs unités : afficher les initiales empilées
            initiales = "".join([u.Unit[0].upper() for u in unites])
            # Utiliser la couleur majoritaire ou de la première
            couleur = Fore.BLUE if unites[0].equipe == 0 else Fore.RED
            grille_affichage[y][x] = f"{couleur}{initiales[:3]:^3}{Style.RESET_ALL}"  # Max 3 lettres

    # 4. Afficher la grille
    print("--- Champ de Bataille ---")
    for ligne in grille_affichage:
        print("".join(ligne))

    # 5. Afficher les points de vie des unités VIVANTES
    print("\n--- Santé des Unités ---")
    unites_vivantes = [u for u in jeu.unites if u.alive]
    
    if not unites_vivantes:
        print("Aucune unité vivante sur le champ de bataille.")
    else:
        for unite in unites_vivantes:
            couleur = Fore.BLUE if unite.equipe == 0 else Fore.RED
            x, y = unite.coords
            if DEBUG == 1:print(f"{couleur}{unite.Unit} (equipe {unite.equipe}) : {unite.HP} HP, position : {x:.1f}, {y:.1f}){Style.RESET_ALL}")