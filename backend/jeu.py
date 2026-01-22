# backend/jeu.py

import math
from backend.carte import Carte
from backend.Units import Unit


class Jeu:
    def __init__(self):
        self.carte = Carte(largeur=30, hauteur=30)
        self.unites = []
        self._tour = 0

    def ajouter_unite(self, nom_unite: str, x: int, y: int, equipe: int = 0):
        if self.carte.est_dans_grille(x, y):
            nouvelle_unite = Unit(nomUnite=nom_unite)
            nouvelle_unite.equipe = equipe
            nouvelle_unite.coords = (float(x), float(y))
            self.unites.append(nouvelle_unite)
            self.carte.placer_unite(nouvelle_unite, x, y)

    def trouver_ennemi_proche(self, unite):
        ennemi_proche = None
        distance_min = float('inf')
        x, y = unite.coords
        
        for autre in self.unites:
            if autre is unite:
                continue
            if autre.equipe == unite.equipe:
                continue
            if not autre.alive:
                continue
            if autre.coords is None:
                continue
            
            autre_x, autre_y = autre.coords
            distance = math.sqrt((autre_x - x)**2 + (autre_y - y)**2)
            
            if distance < distance_min:
                distance_min = distance
                ennemi_proche = autre
        
        if ennemi_proche:
            return ennemi_proche, distance_min
        return None, None

    def deplacer_vers(self, unite, cible_x, cible_y):
        x, y = unite.coords
        dx = cible_x - x
        dy = cible_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 0.1:
            return
        
        vitesse = 2.5
        
        if distance <= vitesse:
            unite.coords = (cible_x, cible_y)
        else:
            ratio = vitesse / distance
            unite.coords = (x + dx * ratio, y + dy * ratio)

    def mettre_a_jour(self):
        self._tour += 1
        unites_actives = [u for u in self.unites if u.alive and u.coords]

        for unite in unites_actives:
            if not unite.alive:
                continue
            
            ennemi, distance = self.trouver_ennemi_proche(unite)
            
            if ennemi is None or distance is None:
                continue
            
            portee = unite.Max_Range if hasattr(unite, 'Max_Range') and unite.Max_Range else 1.5
            
            if distance <= portee:
                unite.target = ennemi
                degats = 5
                if hasattr(unite, 'Attack') and isinstance(unite.Attack, dict):
                    for val in unite.Attack.values():
                        if isinstance(val, (int, float)):
                            degats = max(degats, val)
                
                ennemi.HP -= degats
                
                if ennemi.HP <= 0:
                    ennemi.alive = False
            else:
                ex, ey = ennemi.coords
                self.deplacer_vers(unite, ex, ey)

        self.unites = [u for u in self.unites if u.alive]
