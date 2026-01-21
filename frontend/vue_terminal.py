
import colorama
from colorama import Fore, Back, Style

from backend.carte import Carte

def afficher(jeu):
    colorama.init(autoreset=True)

    carte = jeu.carte
    
    grille_affichage = [[f"{Fore.GREEN} . {Style.RESET_ALL}" for _ in range(carte.largeur)] for _ in range(carte.hauteur)]


    unites_par_case = {}
    for unite in jeu.unites:
        if not unite.alive:
            continue
        
        x_float, y_float = unite.coords
        x_case = round(x_float)
        y_case = round(y_float)
        
        if 0 <= x_case < carte.largeur and 0 <= y_case < carte.hauteur:
            cle = (x_case, y_case)
            if cle not in unites_par_case:
                unites_par_case[cle] = []
            unites_par_case[cle].append(unite)
    
    for (x, y), unites in unites_par_case.items():
        if len(unites) == 1:
            unite = unites[0]
            initiale = unite.Unit[0].upper()
            couleur = Fore.BLUE if unite.equipe == 0 else Fore.RED
            grille_affichage[y][x] = f"{couleur} {initiale} {Style.RESET_ALL}"
        else:
            initiales = "".join([u.Unit[0].upper() for u in unites])
 
            couleur = Fore.BLUE if unites[0].equipe == 0 else Fore.RED
            grille_affichage[y][x] = f"{couleur}{initiales[:3]:^3}{Style.RESET_ALL}"  


    print("--- Champ de Bataille ---")
    for ligne in grille_affichage:
        print("".join(ligne))

  
    print("\n--- Santé des Unités ---")
    unites_vivantes = [u for u in jeu.unites if u.alive]
    
    if not unites_vivantes:
        print("Aucune unité vivante sur le champ de bataille.")
    else:
        for unite in unites_vivantes:
            couleur = Fore.BLUE if unite.equipe == 0 else Fore.RED
            x, y = unite.coords
            print(f"{couleur}{unite.Unit} (equipe {unite.equipe}) : {unite.HP} HP, position : {x:.1f}, {y:.1f}){Style.RESET_ALL}")
