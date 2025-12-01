# Ce fichier contient la classe qui représente le champ de bataille.
from backend.Units import Unit




from backend.Units import Unit

class Carte:
    """
    Représente la carte du jeu, une grille 2D.
    Elle stocke les dimensions et ce qui se trouve sur chaque case.
    """
    def __init__(self, largeur: int, hauteur: int):
        """
        Initialise une nouvelle carte.
        
        Arguments:
            largeur (int): Le nombre de cases en largeur.
            hauteur (int): Le nombre de cases en hauteur.
        """
        self.largeur = largeur
        self.hauteur = hauteur
        # Chaque case contient maintenant une LISTE d'unités
        self.grille = [[[] for _ in range(largeur)] for _ in range(hauteur)]



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


    def get_unites_a(self, x: int, y: int):
        """
        Renvoie la LISTE des unités qui se trouvent aux coordonnées (x, y).
        
        Returns:
            list: La liste des unités trouvées (vide si aucune unité).
        """
        if not self.est_dans_grille(x, y):
            return []
        
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
            # Ajoute l'unité à la liste si elle n'y est pas déjà
            if unite not in self.grille[y][x]:
                self.grille[y][x].append(unite)

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
                
    
                
    
    
