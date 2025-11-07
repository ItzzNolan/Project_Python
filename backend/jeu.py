# backend/jeu.py

import time
from backend.carte import Carte
from backend.Units import Unit  
from frontend.vue_terminal import afficher

class Jeu:
    """
    Classe principale du jeu. Gère la carte, les unités et la boucle de jeu.
    """
    def __init__(self):
        """
        Crée une Carte et une liste d'unités.
        """
        self.carte = Carte(largeur=25, hauteur=15)
        self.unites = []
        self._tour = 1

    def ajouter_unite(self, nom_unite: str, x: int, y: int, equipe: int = 0):
        """
        Crée une unité, l'ajoute à la liste du jeu et la place sur la carte.
        
        Arguments:
            nom_unite: Le type d'unité à créer
            x, y: Position initiale
            equipe: 0 pour équipe bleue, 1 pour équipe rouge
        """
        if self.carte.est_dans_grille(x, y):
            nouvelle_unite = Unit(nomUnite=nom_unite)
            nouvelle_unite.equipe = equipe
            nouvelle_unite.coords = (x, y)
            
            self.unites.append(nouvelle_unite)
            self.carte.placer_unite(nouvelle_unite, x, y)
            print(f"{nom_unite} (équipe {equipe}) ajouté en ({x}, {y}).")
        else:
            print(f"ERREUR : Impossible d'ajouter {nom_unite} en ({x}, {y}), hors de la carte.")

    def est_termine(self) -> bool:
        """
        Vérifie si la partie est terminée (une équipe n'a plus d'unités vivantes).
        """
        # Compter les unités vivantes par équipe
        equipe_0_vivante = any(u.alive and u.equipe == 0 for u in self.unites)
        equipe_1_vivante = any(u.alive and u.equipe == 1 for u in self.unites)
        
        # La partie est terminée si l'une des équipes n'a plus d'unités vivantes
        if not equipe_0_vivante:
            print("\n*** L'EQUIPE ROUGE (1) A GAGNE ! ***")
            return True
        if not equipe_1_vivante:
            print("\n*** L'EQUIPE BLEUE (0) A GAGNE ! ***")
            return True
            
        return False

    def trouver_ennemi_proche(self, unite):
        """
        Trouve l'ennemi le plus proche d'une unité.
        
        Returns:
            tuple: (ennemi, distance) ou (None, None) si aucun ennemi
        """
        ennemi_proche = None
        distance_min = float('inf')
        
        x, y = unite.coords
        
        for autre in self.unites:
            # Ignorer si même équipe ou mort
            if autre.equipe == unite.equipe or not autre.alive:
                continue
            
            # Calculer la distance euclidienne
            autre_x, autre_y = autre.coords
            import math
            distance = math.sqrt((autre_x - x)**2 + (autre_y - y)**2)
            
            if distance < distance_min:
                distance_min = distance
                ennemi_proche = autre
        
        return ennemi_proche, distance_min if ennemi_proche else (None, None)

    def deplacer_unite(self, unite, cible_x, cible_y):
        """
        Déplace une unité d'une case vers sa cible.
        """
        # Retirer de l'ancienne position
        self.carte.retirer_unite(unite)
        
        x, y = unite.coords
        
        # Calculer la direction (un pas à la fois)
        dx = cible_x - x
        dy = cible_y - y
        
        # Calculer la distance
        import math
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance == 0:
            # Déjà sur place
            self.carte.placer_unite(unite, x, y)
            return
        
        # Déplacement limité par la vitesse de l'unité
        vitesse = unite.Speed if hasattr(unite, 'Speed') and unite.Speed else 1.0
        
        if distance <= vitesse:
            # Peut atteindre la cible en un tour
            nouvelle_x = cible_x
            nouvelle_y = cible_y
        else:
            # Se déplace de "vitesse" cases dans la direction de la cible
            ratio = vitesse / distance
            nouvelle_x = x + dx * ratio
            nouvelle_y = y + dy * ratio
        
        # Mettre à jour la position
        unite.coords = (nouvelle_x, nouvelle_y)
        
        # Placer à la nouvelle position
        self.carte.placer_unite(unite, int(nouvelle_x), int(nouvelle_y))

    def mettre_a_jour(self):
        """
        Méthode principale appelée à chaque tour.
        Gère l'affichage, le déplacement et les combats.
        """
        print(f"\n{'='*50}")
        print(f"--- TOUR {self._tour} ---")
        print(f"{'='*50}")

        # 1. AFFICHER L'ÉTAT ACTUEL
        afficher(self)

        # 2. LOGIQUE DU JEU : Chaque unité agit
        for unite in self.unites:
            # Ignorer les unités mortes
            if not unite.alive:
                continue
            
            # Trouver l'ennemi le plus proche
            ennemi, distance = self.trouver_ennemi_proche(unite)
            
            if ennemi is None:
                continue  # Pas d'ennemi trouvé
            
            # Vérifier la portée de l'unité
            portee = unite.Max_Range if unite.Max_Range else 0
            
            # Pour les unités de mêlée (portée 0), elles doivent être sur la même case
            if portee == 0:
                # Vérifier si l'ennemi est sur la même case (distance < 0.1 pour tolérance flottante)
                if distance < 0.1:
                    # ATTAQUE AU CORPS A CORPS !
                    print(f"[ATTAQUE MELEE] {unite.Unit} (equipe {unite.equipe}) attaque {ennemi.Unit} (equipe {ennemi.equipe}) sur la meme case")
                    
                    unite.target = ennemi
                    unite.inflict_damage()
                    
                    print(f"   {ennemi.Unit} a maintenant {max(0, ennemi.HP)} HP")
                    
                    if not ennemi.alive:
                        print(f"[MORT] {ennemi.Unit} est mort !")
                        self.carte.retirer_unite(ennemi)
                else:
                    # SE DÉPLACER vers l'ennemi pour être sur la même case
                    ennemi_x, ennemi_y = ennemi.coords
                    print(f"[DEPLACEMENT] {unite.Unit} (equipe {unite.equipe}) se deplace vers {ennemi.Unit}")
                    self.deplacer_unite(unite, ennemi_x, ennemi_y)
                    print(f"   Nouvelle position : {unite.coords}")
            else:
                # Pour les unités à distance
                if distance <= portee:
                    # ATTAQUE A DISTANCE !
                    print(f"[ATTAQUE DISTANCE] {unite.Unit} (equipe {unite.equipe}) attaque {ennemi.Unit} (equipe {ennemi.equipe}) a distance {distance:.1f}")
                    
                    unite.target = ennemi
                    unite.inflict_damage()
                    
                    print(f"   {ennemi.Unit} a maintenant {max(0, ennemi.HP)} HP")
                    
                    if not ennemi.alive:
                        print(f"[MORT] {ennemi.Unit} est mort !")
                        self.carte.retirer_unite(ennemi)
                else:
                    # SE DÉPLACER vers la portée d'attaque
                    ennemi_x, ennemi_y = ennemi.coords
                    print(f"[DEPLACEMENT] {unite.Unit} (equipe {unite.equipe}) se deplace vers portee d'attaque")
                    self.deplacer_unite(unite, ennemi_x, ennemi_y)
                    print(f"   Nouvelle position : {unite.coords}")

        # 3. Nettoyer les unités mortes
        self.unites = [u for u in self.unites if u.alive]

