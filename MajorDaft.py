#Ci-dessous se trouve la classe Major DAFT.
#Nolan a créé une version de ce commandant plus intelligente, donc j’ai modifié un peu le code.
#Vous pouvez proposer un nouveau nom pour le commandant de Nolan.

class MajorDaft:
    def __init__(self, portee):
        self.portee = portee

    def distance(self, u1, u2):
        return abs(u1.x - u2.x) + abs(u1.y - u2.y)   # distance 

    def direction_vers(self, u1, u2):
        """Retourne un vecteur (dx, dy) indiquant la direction vers l’ennemi."""
        dx = 0
        dy = 0
        if u2.x > u1.x:
            dx = 1
        elif u2.x < u1.x:
            dx = -1

        if u2.y > u1.y:
            dy = 1
        elif u2.y < u1.y:
            dy = -1

        return (dx, dy)

    def decider_actions(self, unites_alliees, unites_ennemies):
        actions = []

        for u_allie in unites_alliees:

            # Trouver l'ennemi le plus proche
            ennemi_proche = min(
                unites_ennemies,
                key=lambda u_ennemi: self.distance(u_allie, u_ennemi)
            )
            dist = self.distance(u_allie, ennemi_proche)

            #  Si l’ennemi est à portée → attaquer
            if dist <= self.portee:
                actions.append(('ATTAQUER', ennemi_proche))

            # Sinon → se déplacer vers l'ennemi
            else:
                direction = self.direction_vers(u_allie, ennemi_proche)
                actions.append(('DEPLACER', direction))

        return actions

