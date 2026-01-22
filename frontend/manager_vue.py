# frontend/manager_vue.py

import pygame
from frontend.vue_pygame import VuePygame
from frontend.vue_terminal import VueTerminal


class ManagerVue:
    def __init__(self, jeu):
        self.jeu = jeu
        
        # On initialise la vue pygame
        self.vue_pygame = VuePygame(jeu.carte.largeur, jeu.carte.hauteur)
        
        # Vue terminal
        self.vue_terminal = VueTerminal()
        
        # Le mode initial est Pygame
        self.mode_actuel = "PYGAME"

    def changer_mode(self):
        """Bascule entre le mode PYGAME et le mode TERMINAL."""
        if self.mode_actuel == "PYGAME":
            self.mode_actuel = "TERMINAL"
            print("--- Passage en Vue Terminal ---")
        else:
            self.mode_actuel = "PYGAME"
            print("--- Passage en Vue Pygame ---")

    def afficher(self):
        """Appelle la fonction d'affichage du mode actuel."""
        if self.mode_actuel == "PYGAME":
            self.vue_pygame.afficher(self.jeu)
        else:
            # Mode Terminal: on utilise l'ecran pygame pour afficher la grille
            self.vue_terminal.afficher(self.vue_pygame.screen, self.jeu)
