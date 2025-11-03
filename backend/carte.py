# Ce fichier contient la classe qui représente le champ de bataille.

from backend.Units import Units

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

    def get_unite_a(self, x: int, y: int):
        """
        Renvoie l'objet unité qui se trouve aux coordonnées (x, y).
        
        Returns:
            Unite: L'objet unité trouvé, ou None si la case est vide ou en dehors de la carte.
        """
        if not self.est_dans_grille(x, y):
            return None
        
        return self.grille[y][x]
    
    def placer_unite(self, unite, x: int, y: int):
        """
        Place une unité aux coordonnées (x, y) sur la carte.
        
        Arguments:
            unite (Unite): L'unité à placer.
            x (int): La coordonnée x.
            y (int): La coordonnée y.
        """
        if self.est_dans_grille(x, y):
            self.grille[y][x] = unite

    def retirer_unite(self, unite):
        """
        Retire une unité de la carte.
        
        Arguments:
            unite (Unite): L'unité à retirer.
        """
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.grille[y][x] == unite:
                    self.grille[y][x] = None
                    return
                
    
                
    
    