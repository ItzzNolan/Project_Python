import colorama
from colorama import Fore, Style

# la VRAIE classe Carte, car elle existe déjà et elle est fonctionnelle.
from backend.carte import Carte

# --- SECTION DE SIMULATION (CODE TEMPORAIRE) ---
# Le but de cette classe est de simuler une "Unité" pour que notre fonction tant que la vraie ne soit complète.

class FausseUnite:
    def __init__(self, nom: str, pv: int, equipe: int, x: int, y: int):
        self.nom = nom                  
        self.points_de_vie = pv         
        self.equipe = equipe            
        self.x = x                      
        self.y = y                      



def afficher_jeu(carte: Carte, unites: list[FausseUnite]):
    """
    Affiche l'état complet du jeu dans le terminal, en respectant les exigences.
    
    Arguments:
        carte (Carte): L'objet carte réel du jeu.
        unites (list): Une liste d'objets (pour l'instant, nos FaussesUnites).
    """
  
    # autoreset=True évite que tout le terminal reste coloré après notre affichage.
    colorama.init(autoreset=True)

    # 1. On prépare une "toile" vide : une grille de texte remplie de points.
    # C'est plus simple que d'imprimer case par case.
    grille_affichage = [[" . " for _ in range(carte.largeur)] for _ in range(carte.hauteur)]

    # 2. On "dessine" nos unités sur cette toile.
    for unite in unites:
        # On vérifie que l'unité est bien dans les limites de la carte
        if 0 <= unite.x < carte.largeur and 0 <= unite.y < carte.hauteur:
            
            # On prend la première lettre du nom (C pour Chevalier, P pour Piquier)
            initiale = unite.nom[0]
            
            # On met en majuscule pour l'équipe 1, minuscule pour l'équipe 2 (comme dans l'exemple du prof)
            lettre = initiale.upper() if unite.equipe == 1 else initiale.lower()
            
            # On choisit la couleur en fonction de l'équipe
            couleur = Fore.BLUE if unite.equipe == 1 else Fore.RED
            
            # On place le caractère coloré dans notre grille de texte, à la bonne position
            grille_affichage[unite.y][unite.x] = f"{couleur}{lettre}{Style.RESET_ALL} "

    # 3. On affiche le résultat final.
    print("--- Champ de Bataille ---")
    for ligne in grille_affichage:
        # "".join(ligne) est une façon très efficace d'assembler toutes les cases d'une ligne
        # en une seule chaîne de caractères avant de l'imprimer.
        print("".join(ligne))

    # 4. On affiche la liste des points de vie sous la carte, comme demandé.
    print("\n--- Santé des Unités ---")
    for unite in unites:
        couleur = Fore.BLUE if unite.equipe == 1 else Fore.RED
        print(f"{couleur}{unite.nom} (équipe {unite.equipe}) aux coordonnées ({unite.x},{unite.y}) : {unite.points_de_vie} PV")