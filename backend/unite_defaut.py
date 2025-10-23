class Unite_defaut:
    """
    correspond à une unité par défaut.
    Elle stocke les HP, point d'attaque, point de défense...
    """

    def __init__(self, HP: int, attaque: int, defense : int, emplacement: tuple, type_unite: str = "chevalier"):
        """
        Initialise une nouvelle unité.
        
        Args:
            HP (int): Le nombre point de vie.
            attaque (int): Le nombre point d'attaque.
            defense (int): Le nombre point de défense.
            emplacement (tuple): La position initiale de l'unité.
        """
        self.HP = HP
        self.attaque = attaque
        self.defense = defense
        self.emplacement = emplacement
        self.type_unite = type_unite
        

    def degats(self, attaque_adversaire: int):
        """
        Calcule les dégats subis par l'unité en fonction de l'attaque de l'adversaire.
       
        Args:
            attaque_adversaire (int): Le nombre point d'attaque de l'adversaire.

        Returns:
            int: Les dégats subis par l'unité.
        """

        degats_subis = attaque_adversaire - self.defense
        if degats_subis > 0:
            self.HP = degats_subis
        return degats_subis 
    
    def est_vivant(self) -> bool:
        """
        Vérifie si l'unité est toujours vivante.

        Returns:
            bool: True si l'unité a des points de vie supérieurs à 0, 
                    False sinon.
        """
        if self.HP > 0:
            return True
        return False
    
    def deplacement(self):
        """
        Méthode de déplacement par défaut: avance tout droit.

        Returns:
            tuple: La nouvelle position de l'unité après déplacement.
        """
        x, y = self.emplacement
        self.emplacement = (x + 1, y)
        return self.emplacement
    
    def __str__(self):
        return f"Unité de type {self.type_unite} | HP: {self.HP} | Attaque: {self.attaque} | Défense: {self.defense} | Emplacement: {self.emplacement}"
    
if __name__ == "__main__":
    unite = Unite_defaut(HP=100, attaque=20, defense=10, emplacement=(0, 0))
    print(unite)
    print("Dégats subis:", unite.degats(attaque_adversaire=25))
    print("Est vivant?", unite.est_vivant())
    print("Nouvel emplacement après déplacement:", unite.deplacement())
    print(unite)


    
    
        
    
    
