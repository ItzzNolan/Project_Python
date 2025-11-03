# Ce fichier contient la classe qui représente le champ de bataille.
from backend.Units import Unit




class Carte:
    """
    Représente la carte du jeu, une grille 2D.
    Elle stocke les dimensions et ce qui se trouve sur chaque case.
    """
    """Le constructeur de la classe Carte."""
    def __init__(self, largeur: int, hauteur: int):
        """
        Initialise une nouvelle carte.
        
        Arguments:
            largeur (int): Le nombre de cases en largeur.
            hauteur (int): Le nombre de cases en hauteur.
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[None for _ in range(largeur)] for _ in range(hauteur)]



    def est_dans_grille(self, x: int, y: int) -> bool:
        """
        Vérifie si les coordonnées (x, y) sont à l'intérieur des limites de la carte.
        
        Returns:
            bool: True si les coordonnées sont valides, False sinon.
        """
        return 0 <= x < self.largeur and 0 <= y < self.hauteur
    

    def placer_unite(self, unite: Unit, x: int, y: int) -> bool:
    # On ajoute la condition cruciale : "and self.grille[y][x] is None"
        if self.est_dans_grille(x, y) and self.grille[y][x] is None:
            self.grille[y][x] = unite
            return True
    
     # Si l'une des deux conditions est fausse, on arrive ici et on renvoie False
        return False


    def retirer_unite(self, unite: Unit) -> bool:
        """
        Retire une unité de la carte. Pour cela, elle parcourt la grille pour trouver l'unité.

        Args:
            unite (Unite): L'instance de l'unité à retirer.
            
        Returns:
            bool: True si l'unité a été trouvée et retirée, False sinon.
        """
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.grille[y][x] == unite:
                    self.grille[y][x] = None
                    # L'unité a été trouvée et retirée, on peut arrêter la recherche
                    return True
        # Si on termine les boucles sans trouver l'unité, c'est qu'elle n'était pas sur la carte
        return False


    def get_unite_a(self, x: int, y: int):
        """
        Renvoie l'objet unité qui se trouve aux coordonnées (x, y).
        
        Returns:
            Unite: L'objet unité trouvé, ou None si la case est vide ou en dehors de la carte.
        """
        if not self.est_dans_grille(x, y):
            return None
        
        return self.grille[y][x]