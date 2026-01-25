from backend.Units import Unit
class Carte:
    def __init__(self, largeur: int, hauteur: int):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[[] for _ in range(largeur)] for _ in range(hauteur)]

    def est_dans_grille(self, x: int, y: int) -> bool:
        return 0 <= x < self.largeur and 0 <= y < self.hauteur
    def get_unites_a(self, x: int, y: int):
        if not self.est_dans_grille(x, y):
            return []
        return self.grille[y][x]
    def placer_unite(self, unite, x: int, y: int):
        if self.est_dans_grille(x, y):
            if unite not in self.grille[y][x]:
                self.grille[y][x].append(unite)
    def retirer_unite(self, unite):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if self.grille[y][x] == unite:
                    self.grille[y][x] = None
                    return
                
    
                
    
    
